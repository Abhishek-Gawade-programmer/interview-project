from typing import List, Optional
from pydantic import BaseModel

from app.schemas.permission import Permission


# Shared properties
class RoleBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    name: str


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    pass


# Properties shared by models stored in DB
class RoleInDBBase(RoleBase):
    id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Role(RoleInDBBase):
    permissions: List[Permission] = []


# Properties stored in DB
class RoleInDB(RoleInDBBase):
    pass
