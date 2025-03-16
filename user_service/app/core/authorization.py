from oso import Oso
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import Optional, List

from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


class Authorization:
    def __init__(self):
        self.oso = Oso()
        self.oso.register_class(User)
        self.oso.register_class(Role)
        self.oso.register_class(Permission)
        self.load_policy()

    def load_policy(self):
        """Load the Polar policy file."""
        self.oso.load_files(["app/core/policy.polar"])

    def authorize(self, user: User, action: str, resource: any, db: Session):
        """Check if the user is authorized to perform the action on the resource."""
        if not self.oso.is_allowed(user, action, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return True

    def get_authorized_resources(self, user: User, action: str, resource_cls, db: Session):
        """Get all resources of a type that a user is authorized to perform an action on."""
        query = db.query(resource_cls)
        authorized_resources = []
        
        for resource in query.all():
            if self.oso.is_allowed(user, action, resource):
                authorized_resources.append(resource)
                
        return authorized_resources


# Create a global instance
authorization = Authorization() 