"""主程序入口"""
from src.core.document_parser import DocumentParser
from src.core.text_chunker import TextChunker
from src.models.model_manager import ModelManager
from src.core.vector_store import VectorStore
from src.utils.logger import logger
import os

def initialize_documents():
    """初始化文档处理"""
    from preprocess_docs import process_documents
    process_documents()

def main():
    """主函数"""
    logger.info("文档检索系统启动")
    
    # 这里可以添加其他初始化逻辑
    pass

if __name__ == "__main__":
    main()