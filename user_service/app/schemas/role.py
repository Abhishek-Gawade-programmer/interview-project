from typing import List, Optional
from pydantic import BaseModel

from app.schemas.permission import PermissionBase


# Shared properties
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    name: Optional[str] = None


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Role(RoleInDBBase):
    permissions: List[PermissionBase] = []


# Additional properties stored in DB
class RoleInDB(RoleInDBBase):
    pass 