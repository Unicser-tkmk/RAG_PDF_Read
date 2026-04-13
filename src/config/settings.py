"""应用配置设置"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # 模型配置
    EMBEDDING_MODEL_NAME: str = "Qwen/Qwen3-Embedding-0.6B"
    RERANKER_MODEL_NAME: str = "Qwen/Qwen3-Reranker-0.6B"
    
    # 文档处理配置
    CHUNK_SIZE: int = 512
    OVERLAP_SIZE: int = 50
    MAX_TABLE_ROWS: int = 20
    
    # 向量数据库配置
    CHROMA_DB_PATH: str = "./data/chroma_db"
    COLLECTION_NAME: str = "documents"
    
    # API配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()