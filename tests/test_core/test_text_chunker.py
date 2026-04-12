"""文本分块器测试"""
import pytest
from src.core.text_chunker import TextChunker

def test_text_chunker_initialization():
    """测试文本分块器初始化"""
    chunker = TextChunker()
    assert chunker.chunk_size == 512
    assert chunker.overlap == 50

def test_semantic_chunking_empty():
    """测试空文本分块"""
    chunker = TextChunker()
    result = chunker.semantic_chunking("")
    assert result == []

def test_split_by_sections():
    """测试章节分割"""
    chunker = TextChunker()
    text = "第一章 引言\n这是第一章内容。\n第二章 方法\n这是第二章内容。"
    sections = chunker.split_by_sections(text)
    assert len(sections) >= 1