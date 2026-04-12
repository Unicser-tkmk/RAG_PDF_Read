"""查询路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.core.vector_store import VectorStore
from src.models.model_manager import ModelManager
from src.core.query_processor import QueryProcessor
from src.utils.logger import logger

# 全局实例（在实际生产环境中应该使用依赖注入）
_vector_store = None
_model_manager = None
_query_processor = None

def get_query_processor():
    """获取查询处理器实例"""
    global _vector_store, _model_manager, _query_processor
    
    if _query_processor is None:
        try:
            _vector_store = VectorStore()
            _model_manager = ModelManager()
            _model_manager.load_embedding_model("Qwen/Qwen3-Embedding-0.6B")
            _vector_store.set_model(_model_manager.embedding_model)
            _query_processor = QueryProcessor(_vector_store, _model_manager)
            logger.info("查询处理器初始化完成")
        except Exception as e:
            logger.error(f"查询处理器初始化失败: {str(e)}")
            raise
    
    return _query_processor

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class SearchResult(BaseModel):
    id: str
    document: str
    metadata: dict
    score: float
    original_query: str

class QueryResponse(BaseModel):
    results: List[SearchResult]
    total: int

router = APIRouter()

@router.post("/search")
async def search_documents(request: QueryRequest):
    """搜索文档"""
    try:
        query_processor = get_query_processor()
        results = query_processor.search(request.query, request.top_k)
        
        # 转换为响应格式
        formatted_results = []
        for result in results:
            formatted_results.append(SearchResult(
                id=result['id'],
                document=result['document'],
                metadata=result['metadata'],
                score=result['score'],
                original_query=result['original_query']
            ))
        
        response = QueryResponse(
            results=formatted_results,
            total=len(formatted_results)
        )
        
        logger.info(f"查询完成: '{request.query}', 返回 {len(results)} 个结果")
        return response
        
    except Exception as e:
        logger.error(f"查询处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))