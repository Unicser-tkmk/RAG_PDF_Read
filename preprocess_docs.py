#!/usr/bin/env python3
"""
文档预处理脚本 - 首次运行时使用
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.document_parser import DocumentParser
from src.core.text_chunker import TextChunker
from src.models.model_manager import ModelManager
from src.core.vector_store import VectorStore
from src.utils.logger import setup_logger

logger = setup_logger()

def process_documents():
    """处理文档并构建向量数据库"""
    try:
        # 初始化组件
        parser = DocumentParser()
        chunker = TextChunker()
        model_manager = ModelManager()
        vector_store = VectorStore()
        
        # 加载模型
        print("📥 加载嵌入模型...")
        model_manager.load_embedding_model("Qwen/Qwen3-Embedding-0.6B")
        vector_store.set_model(model_manager.embedding_model)
        
        # 获取文档列表
        doc_dir = "data/input/documents/"
        if not os.path.exists(doc_dir):
            os.makedirs(doc_dir)
            print(f"📁 请将PDF文档放入 {doc_dir} 目录")
            return
        
        pdf_files = [f for f in os.listdir(doc_dir) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"📝 没有找到PDF文档，请将文档放入 {doc_dir}")
            return
        
        print(f"📄 发现 {len(pdf_files)} 个PDF文档")
        
        # 处理每个文档
        all_chunks = []
        for pdf_file in pdf_files:
            file_path = os.path.join(doc_dir, pdf_file)
            print(f"🔍 处理文档: {pdf_file}")
            
            # 解析文档
            text_content, tables = parser.parse_pdf(file_path)
            
            # 分块处理
            for item in text_content:
                chunks = chunker.semantic_chunking(item['text'], item.get('tables'))
                for chunk in chunks:
                    all_chunks.append({
                        'text': chunk,
                        'source': pdf_file,
                        'page': item['page'],
                        'table': item.get('tables')
                    })
        
        print(f"📦 总共生成 {len(all_chunks)} 个文档块")
        
        # 存储到向量数据库
        print("💾 存储到向量数据库...")
        vector_store.store_documents(all_chunks)
        
        print("✅ 文档处理完成！")
        logger.info("文档预处理完成")
        
    except Exception as e:
        print(f"❌ 处理文档时出错: {str(e)}")
        logger.error(f"文档预处理失败: {str(e)}")
        raise

if __name__ == "__main__":
    process_documents()