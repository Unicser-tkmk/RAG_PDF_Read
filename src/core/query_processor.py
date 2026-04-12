"""查询处理模块"""
from typing import List, Dict, Any
from src.core.vector_store import VectorStore
from src.models.model_manager import ModelManager
from src.utils.logger import logger

class QueryProcessor:
    """查询处理器"""
    
    def __init__(self, vector_store: VectorStore, model_manager: ModelManager):
        self.vector_store = vector_store
        self.model_manager = model_manager
    
    def multi_query_decomposition(self, query: str) -> List[str]:
        """多问题查询拆解（简化实现）"""
        # 简单的多问题检测：基于问号、分号等
        if '?' in query or '？' in query:
            sub_queries = [q.strip() for q in re.split(r'[?？]', query) if q.strip()]
            return sub_queries if len(sub_queries) > 1 else [query]
        elif ';' in query or '；' in query:
            sub_queries = [q.strip() for q in re.split(r'[;；]', query) if q.strip()]
            return sub_queries if len(sub_queries) > 1 else [query]
        else:
            return [query]
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """执行检索"""
        try:
            # 检查是否为多问题查询
            sub_queries = self.multi_query_decomposition(query)
            
            all_results = []
            for sub_query in sub_queries:
                logger.info(f"处理子查询: {sub_query}")
                results = self.vector_store.search(sub_query, top_k)
                # 标记子查询来源
                for result in results:
                    result['original_query'] = sub_query
                all_results.extend(results)
            
            # 去重并排序（简化版）
            unique_results = self._deduplicate_results(all_results)
            sorted_results = sorted(unique_results, key=lambda x: x['score'], reverse=True)
            
            return sorted_results[:top_k]
            
        except Exception as e:
            logger.error(f"查询处理失败: {str(e)}")
            raise
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """去重结果"""
        seen_ids = set()
        unique_results = []
        
        for result in results:
            if result['id'] not in seen_ids:
                seen_ids.add(result['id'])
                unique_results.append(result)
        
        return unique_results