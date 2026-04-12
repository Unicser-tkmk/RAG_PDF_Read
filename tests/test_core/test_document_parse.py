"""文档解析器测试"""
import pytest
from src.core.document_parser import DocumentParser

def test_document_parser_initialization():
    """测试文档解析器初始化"""
    parser = DocumentParser()
    assert parser is not None

def test_section_patterns():
    """测试章节模式"""
    parser = DocumentParser()
    assert len(parser.section_patterns) > 0