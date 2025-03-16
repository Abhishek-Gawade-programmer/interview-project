from typing import Optional
from pydantic import BaseModel


# Shared properties
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    resource: str
    action: str


# Properties to receive via API on creation
class PermissionCreate(PermissionBase):
    pass


# Properties to receive via API on update
class PermissionUpdate(PermissionBase):
    name: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None


class PermissionInDBBase(PermissionBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Permission(PermissionInDBBase):
    pass


# Additional properties stored in DB
class PermissionInDB(PermissionInDBBase):
    pass 