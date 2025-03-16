from typing import Optional
from pydantic import BaseModel


# Shared properties
class DocumentBase(BaseModel):
    name: Optional[str] = None
    content_type: Optional[str] = None


# Properties to receive via API on creation
class DocumentCreate(DocumentBase):
    name: str
    content_type: str


# Properties to receive via API on update
class DocumentUpdate(DocumentBase):
    pass


# Properties shared by models stored in DB
class DocumentInDBBase(DocumentBase):
    id: int
    file_path: str
    owner_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Document(DocumentInDBBase):
    pass


# Properties stored in DB
class DocumentInDB(DocumentInDBBase):
    content: Optional[str] = None
    vector_store_path: Optional[str] = None


# Query schema
class DocumentQuery(BaseModel):
    query: str
