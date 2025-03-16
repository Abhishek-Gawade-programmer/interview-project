from typing import Any, Dict, Optional, Union, List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.base import BaseService


class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    def add_permission(self, db: Session, *, role_id: int, permission_id: int) -> Dict[str, Any]:
        role = db.query(Role).get(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        permission = db.query(Permission).get(permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        
        if permission not in role.permissions:
            role.permissions.append(permission)
            db.commit()
            db.refresh(role)
        
        return {"status": "success", "message": "Permission added to role"}

    def remove_permission(self, db: Session, *, role_id: int, permission_id: int) -> Dict[str, Any]:
        role = db.query(Role).get(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        permission = db.query(Permission).get(permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        
        if permission in role.permissions:
            role.permissions.remove(permission)
            db.commit()
            db.refresh(role)
        
        return {"status": "success", "message": "Permission removed from role"}

    def add_user(self, db: Session, *, role_id: int, user_id: int) -> Dict[str, Any]:
        role = db.query(Role).get(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if role not in user.roles:
            user.roles.append(role)
            db.commit()
            db.refresh(user)
        
        return {"status": "success", "message": "User added to role"}

    def remove_user(self, db: Session, *, role_id: int, user_id: int) -> Dict[str, Any]:
        role = db.query(Role).get(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if role in user.roles:
            user.roles.remove(role)
            db.commit()
            db.refresh(user)
        
        return {"status": "success", "message": "User removed from role"}


role_service = RoleService(Role) 