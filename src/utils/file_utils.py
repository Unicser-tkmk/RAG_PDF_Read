"""文件工具"""
import os
from pathlib import Path
from typing import List

def get_pdf_files(directory: str) -> List[str]:
    """获取目录中的所有PDF文件"""
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def ensure_directory_exists(directory: str):
    """确保目录存在"""
    Path(directory).mkdir(parents=True, exist_ok=True)