"""FastAPI主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.document_routes import router as document_router
from src.api.routes.query_routes import router as query_router
from src.utils.logger import logger

app = FastAPI(
    title="Document Retrieval RAG API",
    description="基于RAG的文档检索系统API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(document_router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(query_router, prefix="/api/v1/query", tags=["query"])

@app.get("/")
async def root():
    return {"message": "Document Retrieval RAG System API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

logger.info("API应用初始化完成")