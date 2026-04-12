"""模型管理模块"""
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
from typing import Optional
from src.utils.logger import logger

class ModelManager:
    """统一的模型管理器"""
    
    def __init__(self):
        self.embedding_model: Optional[SentenceTransformer] = None
        self.reranker_model: Optional[AutoModel] = None
        self.tokenizer: Optional[AutoTokenizer] = None
    
    def load_embedding_model(self, model_name: str):
        """加载嵌入模型"""
        try:
            logger.info(f"正在加载嵌入模型: {model_name}")
            self.embedding_model = SentenceTransformer(model_name)
            logger.info("嵌入模型加载完成")
        except Exception as e:
            logger.error(f"加载嵌入模型失败: {str(e)}")
            raise
    
    def load_reranker_model(self, model_name: str):
        """加载重排模型"""
        try:
            logger.info(f"正在加载重排模型: {model_name}")
            self.reranker_model = AutoModel.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            logger.info("重排模型加载完成")
        except Exception as e:
            logger.error(f"加载重排模型失败: {str(e)}")
            raise