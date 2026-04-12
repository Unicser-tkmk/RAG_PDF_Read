# 基于RAG的文档检索系统

## 项目介绍
基于Qwen3模型的文档检索系统，支持PDF文档的智能检索、语义分块、向量存储和重排序功能。

## 技术栈
- Python 3.8+
- FastAPI
- Transformers
- Sentence-Transformers
- ChromaDB
- PyPDF2

## 快速开始

### 环境准备
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt