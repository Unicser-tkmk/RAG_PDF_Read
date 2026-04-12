"""文档解析模块"""
import PyPDF2
import re
from typing import List, Dict, Tuple
from pathlib import Path
from src.utils.logger import logger

class DocumentParser:
    """PDF文档解析器"""
    
    def __init__(self):
        self.section_patterns = [
            r'^第[一二三四五六七八九十\d]+章.*$',
            r'^#{1,6}\s+.*$',
            r'^\d+(\.\d+)*\s+.*$'
        ]
    
    def parse_pdf(self, file_path: str) -> Tuple[List[Dict], List[Dict]]:
        """解析PDF文档，返回文本和表格内容"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []
                tables_data = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        # 提取页面中的表格信息（简化版）
                        tables = self._extract_tables_from_text(text)
                        tables_data.extend(tables)
                        
                        text_content.append({
                            'page': page_num + 1,
                            'text': text,
                            'tables': tables
                        })
                
                logger.info(f"成功解析PDF文件: {file_path}, 共{len(text_content)}页")
                return text_content, tables_data
                
        except Exception as e:
            logger.error(f"解析PDF文件失败 {file_path}: {str(e)}")
            raise
    
    def _extract_tables_from_text(self, text: str) -> List[Dict]:
        """从文本中提取表格信息（简化实现）"""
        # 这里可以集成更复杂的表格检测逻辑
        tables = []
        lines = text.split('\n')
        table_lines = []
        in_table = False
        
        for line in lines:
            # 简单的表格检测：包含多个制表符或对齐的竖线
            if line.count('\t') >= 2 or ('|' in line and line.count('|') >= 3):
                if not in_table:
                    table_lines = []
                    in_table = True
                table_lines.append(line)
            else:
                if in_table and table_lines:
                    tables.append({
                        'content': '\n'.join(table_lines),
                        'type': 'detected_table'
                    })
                    table_lines = []
                    in_table = False
        
        # 处理最后一个表格
        if in_table and table_lines:
            tables.append({
                'content': '\n'.join(table_lines),
                'type': 'detected_table'
            })
        
        return tables