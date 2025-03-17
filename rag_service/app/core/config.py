import secrets
from typing import List, Optional, Union, Dict, Any

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "RAG Service"
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "rag_service"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    USER_SERVICE_URL: str = "http://localhost:8000"
    
    # Document storage settings
    UPLOAD_FOLDER: str = "uploads"
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max upload size
    
    # LLM settings
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # Vector DB settings
    VECTOR_DB_TYPE: str = "chroma"  # Options: chroma, pinecone, etc.
    VECTOR_DB_URL: Optional[str] = None
    VECTOR_DB_PERSIST_DIR: str = "uploads/chroma_db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 