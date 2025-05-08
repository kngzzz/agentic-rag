from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    LLM_MODEL: str = "gpt-4o"
    EMBEDDING_DIM: int = 1536 # Dimension for text-embedding-ada-002
    TAVILY_API_KEY: Optional[str] = None
    
    # Weaviate Cloud settings
    WEAVIATE_URL: str = "20nylijqkocr7uq8hfjva.c0.asia-southeast1.gcp.weaviate.cloud"  # Replace with your actual Weaviate Cloud URL
    WEAVIATE_API_KEY: Optional[str] = None  # Will be set from .env file
    WEAVIATE_INDEX_NAME: str = "Documents"  # Collection name in Weaviate
    WEAVIATE_GRPC_ENABLED: bool = True  # Enable gRPC for v4 client

    class Config:
        env_file = "backend/.env" # Adjusted path

settings = Settings()
