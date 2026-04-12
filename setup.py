from setuptools import setup, find_packages

setup(
    name="document-retrieval-rag",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.35.0", 
        "sentence-transformers>=2.7.0",
        "chromadb>=0.4.0",
        "pypdf>=3.8.0",
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0",
        "pydantic>=2.0.0",
        "python-multipart>=0.0.6",
        "loguru>=0.7.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "python-dotenv>=1.0.0"
    ],
    author="Your Name",
    description="基于RAG的文档检索系统",
    python_requires=">=3.8",
)