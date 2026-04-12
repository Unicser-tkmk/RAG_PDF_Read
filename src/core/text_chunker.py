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
    
    def split_by_sections(self, text: str) -> List[str]:
        """按章节分割"""
        if not text.strip():
            return [""]
        
        # 定义章节标题模式
        section_patterns = [
            r'\n第[一二三四五六七八九十\d]+章\s+[^\n]*',
            r'\n#{1,6}\s+[^\n]*',
            r'\n\d+(\.\d+)*\s+[^\n]*'
        ]
        
        sections = [text]
        
        for pattern in section_patterns:
            new_sections = []
            for section in sections:
                if not section.strip():
                    continue
                # 分割文本
                parts = re.split(f'({pattern})', section)
                # 重新组合章节标题和内容
                i = 0
                while i < len(parts):
                    if i + 1 < len(parts) and re.match(pattern, parts[i + 1]):
                        # 章节标题 + 内容
                        combined = parts[i + 1] + (parts[i + 2] if i + 2 < len(parts) else '')
                        new_sections.append(combined)
                        i += 3
                    else:
                        if parts[i].strip():
                            new_sections.append(parts[i])
                        i += 1
            sections = new_sections
        
        # 清理空字符串
        sections = [s.strip() for s in sections if s.strip()]
        return sections if sections else [text]
    
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