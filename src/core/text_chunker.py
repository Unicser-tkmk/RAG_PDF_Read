"""文本分块模块"""
from typing import List, Dict, Optional
import re
from src.config.settings import settings
from src.utils.logger import logger

class TextChunker:
    """语义分块处理器"""
    
    def __init__(self, chunk_size: Optional[int] = None, overlap: Optional[int] = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.overlap = overlap or settings.OVERLAP_SIZE
        self.sentence_endings = r'[。！？.!?\n]'
    
    def semantic_chunking(self, text: str, metadata: Dict = None) -> List[str]:
        """语义分块策略"""
        if not text.strip():
            return []
        
        # 首先按章节分割
        sections = self.split_by_sections(text)
        
        chunks = []
        for section in sections:
            if len(section) <= self.chunk_size:
                chunks.append(section.strip())
            else:
                # 对长章节进行进一步分块
                section_chunks = self._chunk_long_text(section)
                chunks.extend(section_chunks)
        
        logger.debug(f"文本分块完成，生成 {len(chunks)} 个块")
        return chunks
    
    def split_by_sections(self, text):
        """
        按章节分割文本 - 修复版
        """
        if not text or not isinstance(text, str):
            return []
        
        # 分割规则 - 按多个标准分割
        section_patterns = [
            r'\n\s*\d+\.\s+',  # 1. 2. 3. 等章节号
            r'\n\s*[IVX]+\.?\s+',  # I. II. III. 等罗马数字章节
            r'\n\s*[A-Z]\.\s+',  # A. B. C. 等字母章节
            r'\n\s*第[一二三四五六七八九十\d]+章',  # 第X章
            r'\n\s*第[一二三四五六七八九十\d]+节',  # 第X节
            r'\n\s*#\s+',  # Markdown标题
            r'\n\s*##\s+', 
            r'\n\s*###\s+',
        ]
        
        # 找到所有分割点
        all_splits = []
        for pattern in section_patterns:
            matches = list(re.finditer(pattern, text))
            all_splits.extend([(match.start(), match.end(), match.group()) for match in matches])
        
        # 按位置排序
        all_splits.sort(key=lambda x: x[0])
        
        # 提取段落
        parts = []
        start_pos = 0
    
        for pos, end_pos, header in all_splits:
            # 添加前面的内容
            content = text[start_pos:pos].strip()
            if content:  # 只添加非空内容
                parts.append(content)
            
            # 添加标题
            parts.append(header.strip())
            start_pos = end_pos
        
        # 添加最后剩余内容
        if start_pos < len(text):
            remaining = text[start_pos:].strip()
            if remaining:
                parts.append(remaining)
        
        # 过滤None值并确保都是字符串
        parts = [part if part is not None else '' for part in parts]
        
        # 合并相邻的部分，避免过小的片段 - 安全版本
        merged_parts = []
        i = 0
        while i < len(parts):
            current = parts[i] if i < len(parts) and parts[i] is not None else ''
            
            if i + 1 < len(parts) and parts[i + 1] is not None:
                next_part = parts[i + 1] if parts[i + 1] is not None else ''
            else:
                next_part = ''
            
            # 如果当前部分太短，与下一部分合并
            if len(current.strip()) < 50 and i + 1 < len(parts):
                # 安全地获取下一部分和下下部分
                next_next = ''
                if i + 2 < len(parts) and parts[i + 2] is not None:
                    next_next = parts[i + 2]
                elif i + 2 < len(parts):
                    next_next = ''  # parts[i+2] is None
                
                # 安全地拼接字符串
                combined = str(current) + str(next_part) + str(next_next)
                merged_parts.append(combined.strip())
                i += 3  # 跳过已合并的项
            else:
                merged_parts.append(str(current).strip() if current else '')
                i += 1
        
        # 过滤掉空字符串并返回结果
        result = [part for part in merged_parts if part and len(part.strip()) > 1]
        
        return result
    def _chunk_long_text(self, text: str) -> List[str]:
        """对长文本进行分块"""
        sentences = re.split(self.sentence_endings, text)
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        
        if not sentences:
            return [text[:self.chunk_size]]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # 如果单个句子就超过chunk_size，强制截断
                if len(sentence) > self.chunk_size:
                    chunks.extend(self._split_long_sentence(sentence))
                    current_chunk = ""
                else:
                    current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_long_sentence(self, sentence: str) -> List[str]:
        """分割超长句子"""
        chunks = []
        for i in range(0, len(sentence), self.chunk_size):
            chunks.append(sentence[i:i + self.chunk_size])
        return chunks