from typing import Optional, Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.dependencies.auth import get_current_user
from app.services.rbac.authorization import authorize


def check_permission(resource: str, action: str):
    """
    Dependency to check if the current user has permission to perform an action on a resource.
    """

    def _check_permission(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        """
        Check if the current user has permission to perform the action on the resource.
        """
        # Superusers have all permissions
        if current_user.is_superuser:
            return current_user

        # Check if the user has the required permission
        if not authorize(db, current_user, resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions to {action} {resource}",
            )

        return current_user

    return _check_permission
