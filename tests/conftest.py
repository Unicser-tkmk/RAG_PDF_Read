"""pytest配置"""
import pytest
import os
from pathlib import Path

@pytest.fixture
def test_data_dir():
    """测试数据目录"""
    return Path("tests/test_data")

@pytest.fixture
def sample_text():
    """样本文本"""
    return """
    第一章 引言
    这是一个测试文档。
    包含多个段落和章节。
    
    第二章 方法
    详细描述了实现方法。
    包括算法和流程。
    """

@pytest.fixture
def create_test_pdf(tmp_path):
    """创建测试PDF"""
    import PyPDF2
    from PyPDF2 import PdfWriter
    
    pdf_path = tmp_path / "test.pdf"
    writer = PdfWriter()
    
    # 创建简单的PDF页面
    from PyPDF2.generic import NameObject, TextStringObject
    page = writer.add_blank_page(width=612, height=792)
    
    # 保存PDF
    with open(pdf_path, "wb") as f:
        writer.write(f)
    
    return pdf_path