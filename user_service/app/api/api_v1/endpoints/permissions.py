from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.authorization import authorization
from app.models.permission import Permission
from app.models.user import User
from app.schemas.permission import Permission as PermissionSchema, PermissionCreate, PermissionUpdate
from app.services.permission_service import permission_service

router = APIRouter()


@router.get("/", response_model=List[PermissionSchema])
def read_permissions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.check_permissions(action="read", resource_type="permission")),
) -> Any:
    """
    Retrieve permissions.
    """
    permissions = authorization.get_authorized_resources(current_user, "read", Permission, db)
    return permissions[skip : skip + limit]


@router.post("/", response_model=PermissionSchema)
def create_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_in: PermissionCreate,
    current_user: User = Depends(deps.check_permissions(action="create", resource_type="permission")),
) -> Any:
    """
    Create new permission.
    """
    permission = permission_service.get_by_name(db, name=permission_in.name)
    if permission:
        raise HTTPException(
            status_code=400,
            detail="The permission with this name already exists in the system.",
        )
    permission = permission_service.create(db, obj_in=permission_in)
    return permission


@router.get("/{permission_id}", response_model=PermissionSchema)
def read_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_id: int,
    current_user: User = Depends(deps.check_permissions(action="read", resource_type="permission")),
) -> Any:
    """
    Get permission by ID.
    """
    permission = permission_service.get(db, id=permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    # Check if the user has permission to access this specific permission
    authorization.authorize(current_user, "read", permission, db)
    return permission


@router.put("/{permission_id}", response_model=PermissionSchema)
def update_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_id: int,
    permission_in: PermissionUpdate,
    current_user: User = Depends(deps.check_permissions(action="update", resource_type="permission")),
) -> Any:
    """
    Update a permission.
    """
    permission = permission_service.get(db, id=permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    # Check if the user has permission to update this specific permission
    authorization.authorize(current_user, "update", permission, db)
    permission = permission_service.update(db, db_obj=permission, obj_in=permission_in)
    return permission


@router.delete("/{permission_id}", response_model=PermissionSchema)
def delete_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_id: int,
    current_user: User = Depends(deps.check_permissions(action="delete", resource_type="permission")),
) -> Any:
    """
    Delete a permission.
    """
    permission = permission_service.get(db, id=permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    # Check if the user has permission to delete this specific permission
    authorization.authorize(current_user, "delete", permission, db)
    permission = permission_service.remove(db, id=permission_id)
    return permission 