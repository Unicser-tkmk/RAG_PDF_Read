#!/usr/bin/env python3
"""
文档检索系统启动脚本
"""

import os
import sys
from pathlib import Path
import uvicorn

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """启动服务器"""
    from src.config.settings import settings
    
    print("🚀 启动文档检索系统...")
    print(f"   模型: {settings.EMBEDDING_MODEL_NAME}")
    print(f"   API端口: {settings.API_PORT}")
    print(f"   调试模式: {settings.DEBUG}")
    
    # 创建必要的目录
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data/chroma_db", exist_ok=True)
    
    # 启动FastAPI服务器
    uvicorn.run(
        "src.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )

if __name__ == "__main__":
    main()