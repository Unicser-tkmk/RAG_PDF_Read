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
```

### 模型准备
1. 下载Qwen3模型文件到 `models/` 目录
2. 确保模型目录结构如下：
```
models/
└── Qwen3/
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer.json
    ├── tokenizer_config.json
    └── ...
```

### 文档准备
将需要检索的PDF文档放置在 `data/` 目录下：
```
data/
├── document1.pdf
├── document2.pdf
└── ...
```

## 使用方法

### 1. 文档预处理
在启动服务之前，需要先对文档进行预处理和向量化存储：

```bash
python preprocess_docs.py
```

此脚本会执行以下操作：
- 解析PDF文档
- 智能分块处理（保留语义完整性）
- 生成向量嵌入
- 存储到ChromaDB向量数据库

### 2. 启动服务
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. 使用API接口

#### 检查服务状态
```bash
curl http://localhost:8000/
```

响应示例：
```json
{
  "message": "Document Retrieval RAG System API",
  "status": "running"
}
```

#### 文档检索
```bash
curl.exe -X POST 'http://localhost:8000/api/v1/query/search' -H 'Content-Type: application/json' -d '{\"query\": \"您的查询内容\", \"top_k\": 5}'
```

参数说明：
- `query`: 检索查询文本
- `top_k`: 返回结果数量，默认为5

响应示例：
```json
{
  "results": [
    {
      "id": "chunk_123",
      "document": "这是匹配的文档片段内容...",
      "metadata": {
        "source_document": "example.pdf",
        "page_number": 5,
        "chunk_id": "chunk_123"
      },
      "score": 0.856
    }
  ],
  "total": 1
}
```

### 4. Python客户端使用示例

```python
import requests
import json

def search_documents(query, top_k=5):
    """
    搜索文档
    
    Args:
        query (str): 查询内容
        top_k (int): 返回结果数量
    
    Returns:
        dict: 搜索结果
    """
    url = "http://localhost:8000/api/v1/query/search"
    payload = {
        "query": query,
        "top_k": top_k
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# 使用示例
if __name__ == "__main__":
    results = search_documents("关于产品规格的详细信息", top_k=3)
    
    for i, result in enumerate(results["results"], 1):
        print(f"结果 {i}:")
        print(f"  文档: {result['metadata']['source_document']}")
        print(f"  页码: {result['metadata']['page_number']}")
        print(f"  内容: {result['document'][:100]}...")
        print(f"  相似度: {result['score']:.3f}")
        print("-" * 50)
```

## 系统架构

### 核心组件
- **文档处理器**: 负责PDF解析和智能分块
- **向量存储**: 使用ChromaDB进行高效向量检索
- **检索引擎**: 基于Qwen3模型的语义检索
- **API服务**: FastAPI提供RESTful接口

### 数据流程
1. 文档上传/导入 → 2. 智能分块 → 3. 向量化 → 4. 存储到向量库 → 5. 语义检索 → 6. 结果返回

## 配置说明

### 主要配置文件
`src/config/settings.py` 包含以下配置项：
```python
CHROMA_DB_PATH = "./chroma_db"      # 向量数据库存储路径
COLLECTION_NAME = "documents"       # 向量数据库集合名称
MODEL_PATH = "./models/Qwen3"       # 模型路径
DATA_DIR = "./data"                 # 输入文档目录
UPLOAD_DIR = "./uploads"            # 上传文档目录
CHUNK_SIZE = 512                    # 文档分块大小
CHUNK_OVERLAP = 50                  # 分块重叠大小
```

## 高级功能

### 批量处理
支持批量处理多个文档，自动进行分块和向量化。

### 语义检索
利用Qwen3模型的语义理解能力，实现精准的语义检索。

### 结果重排序
对检索结果进行二次排序，提高准确性。

## 故障排除

### 常见问题

1. **模型加载失败**
   - 检查模型文件是否完整
   - 确认模型路径配置正确
   - 检查内存是否充足

2. **文档解析错误**
   - 确认PDF文档格式正确
   - 检查文档是否损坏
   - 验证文档编码格式

3. **API访问失败**
   - 确认服务已启动
   - 检查端口是否被占用
   - 验证网络连接

### 日志查看
系统日志保存在 `logs/` 目录下，可通过以下方式查看：
```bash
tail -f logs/app.log
```

## 性能优化

- 根据文档大小调整分块参数
- 合理设置top_k参数平衡准确性和性能
- 定期清理向量数据库缓存

## 部署建议

### 生产环境部署
```bash
# 使用Gunicorn部署（Linux/Mac）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Windows环境下使用
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

### Docker部署（可选）
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 开发贡献

欢迎提交Issue和Pull Request。在贡献代码前，请确保：
- 代码遵循PEP 8规范
- 添加适当的单元测试
- 更新相关文档

## 许可证

[MIT License](LICENSE)