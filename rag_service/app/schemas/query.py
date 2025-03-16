from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QueryBase(BaseModel):
    query_text: str
    document_id: Optional[int] = None


class QueryCreate(QueryBase):
    pass


class Query(QueryBase):
    id: int
    response: Optional[str] = None
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True 