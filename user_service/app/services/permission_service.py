from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.services.base import BaseService


class PermissionService(BaseService[Permission, PermissionCreate, PermissionUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.name == name).first()

    def get_by_resource_and_action(
        self, db: Session, *, resource: str, action: str
    ) -> Optional[Permission]:
        return db.query(Permission).filter(
            Permission.resource == resource,
            Permission.action == action
        ).first()


permission_service = PermissionService(Permission) 