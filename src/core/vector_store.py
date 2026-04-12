"""向量存储模块"""
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions
from src.config.settings import settings
from src.utils.logger import logger

class VectorStore:
    """向量数据库操作类"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection_name = settings.COLLECTION_NAME
        self.collection = None
        self.embedding_model = None
    
    def set_model(self, embedding_model):
        """设置嵌入模型"""
        self.embedding_model = embedding_model
    
    def _get_or_create_collection(self):
        """获取或创建集合"""
        if self.collection is None:
            try:
                self.collection = self.client.get_collection(
                    name=self.collection_name
                )
            except ValueError:
                # 集合不存在，创建新集合
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
        return self.collection
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """生成文本嵌入向量"""
        if self.embedding_model is None:
            raise ValueError("嵌入模型未设置")
        
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"生成嵌入向量失败: {str(e)}")
            raise
    
    def store_documents(self, chunks_with_metadata: List[Dict]):
        """存储文档块到向量数据库"""
        if not chunks_with_metadata:
            logger.warning("没有文档块需要存储")
            return
        
        collection = self._get_or_create_collection()
        
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk_info in enumerate(chunks_with_metadata):
            chunk_id = f"chunk_{i}"
            ids.append(chunk_id)
            documents.append(chunk_info['text'])
            metadatas.append({
                'source_document': chunk_info['source'],
                'page_number': chunk_info['page'],
                'chunk_id': chunk_id,
                'has_table': bool(chunk_info.get('table'))
            })
        
        # 生成嵌入向量
        logger.info(f"正在生成 {len(documents)} 个文档块的嵌入向量...")
        embeddings = self.generate_embeddings(documents)
        
        # 存储到向量数据库
        try:
            collection.add(
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents,
                ids=ids
            )
            logger.info(f"成功存储 {len(ids)} 个文档块到向量数据库")
        except Exception as e:
            logger.error(f"存储文档块失败: {str(e)}")
            raise
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """执行向量检索"""
        collection = self._get_or_create_collection()
        
        # 生成查询向量
        query_embedding = self.generate_embeddings([query])[0]
        
        # 执行相似度搜索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"]
        )
        
        # 格式化结果
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'score': 1.0 - results['distances'][0][i]  # 转换为相似度分数
            })
        
        return formatted_results