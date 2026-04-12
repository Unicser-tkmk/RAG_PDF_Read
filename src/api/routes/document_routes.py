"""文档路由"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from src.utils.file_utils import ensure_directory_exists
from src.utils.logger import logger

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传文档"""
    try:
        # 验证文件类型
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF文件")
        
        # 确保上传目录存在
        upload_dir = "data/input/documents"
        ensure_directory_exists(upload_dir)
        
        # 保存文件
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"文档上传成功: {file.filename}")
        return JSONResponse(
            status_code=200,
            content={
                "message": "文档上传成功",
                "filename": file.filename,
                "file_path": file_path
            }
        )
        
    except Exception as e:
        logger.error(f"文档上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))