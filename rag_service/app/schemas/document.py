from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ChunkBase(BaseModel):
    content: str
    embedding_id: Optional[str] = None


class ChunkCreate(ChunkBase):
    pass


class Chunk(ChunkBase):
    id: int
    document_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    title: str
    content: Optional[str] = None
    file_type: Optional[str] = None


class DocumentCreate(DocumentBase):
    user_id: int


class DocumentUpdate(DocumentBase):
    title: Optional[str] = None
    embedding_status: Optional[bool] = None


class Document(DocumentBase):
    id: int
    file_path: Optional[str] = None
    embedding_status: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    chunks: List[Chunk] = []

    class Config:
        orm_mode = True 