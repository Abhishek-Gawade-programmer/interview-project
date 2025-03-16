from typing import Optional
from pydantic import BaseModel


# Shared properties
class PermissionBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None


# Properties to receive via API on creation
class PermissionCreate(PermissionBase):
    name: str
    resource: str
    action: str


# Properties to receive via API on update
class PermissionUpdate(PermissionBase):
    pass


# Properties shared by models stored in DB
class PermissionInDBBase(PermissionBase):
    id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Permission(PermissionInDBBase):
    pass


# Properties stored in DB
class PermissionInDB(PermissionInDBBase):
    pass
