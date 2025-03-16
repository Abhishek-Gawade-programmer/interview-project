from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.authorization import authorization
from app.models.role import Role
from app.models.user import User
from app.schemas.role import Role as RoleSchema, RoleCreate, RoleUpdate
from app.services.role_service import role_service

router = APIRouter()


@router.get("/", response_model=List[RoleSchema])
def read_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.check_permissions(action="read", resource_type="role")),
) -> Any:
    """
    Retrieve roles.
    """
    roles = authorization.get_authorized_resources(current_user, "read", Role, db)
    return roles[skip : skip + limit]


@router.post("/", response_model=RoleSchema)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: RoleCreate,
    current_user: User = Depends(deps.check_permissions(action="create", resource_type="role")),
) -> Any:
    """
    Create new role.
    """
    role = role_service.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists in the system.",
        )
    role = role_service.create(db, obj_in=role_in)
    return role


@router.get("/{role_id}", response_model=RoleSchema)
def read_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: User = Depends(deps.check_permissions(action="read", resource_type="role")),
) -> Any:
    """
    Get role by ID.
    """
    role = role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    # Check if the user has permission to access this specific role
    authorization.authorize(current_user, "read", role, db)
    return role


@router.put("/{role_id}", response_model=RoleSchema)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: User = Depends(deps.check_permissions(action="update", resource_type="role")),
) -> Any:
    """
    Update a role.
    """
    role = role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    # Check if the user has permission to update this specific role
    authorization.authorize(current_user, "update", role, db)
    role = role_service.update(db, db_obj=role, obj_in=role_in)
    return role


@router.delete("/{role_id}", response_model=RoleSchema)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: User = Depends(deps.check_permissions(action="delete", resource_type="role")),
) -> Any:
    """
    Delete a role.
    """
    role = role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    # Check if the user has permission to delete this specific role
    authorization.authorize(current_user, "delete", role, db)
    role = role_service.remove(db, id=role_id)
    return role


@router.post("/{role_id}/permissions/{permission_id}")
def add_permission_to_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    permission_id: int,
    current_user: User = Depends(deps.check_permissions(action="update", resource_type="role")),
) -> Any:
    """
    Add a permission to a role.
    """
    return role_service.add_permission(db, role_id=role_id, permission_id=permission_id)


@router.delete("/{role_id}/permissions/{permission_id}")
def remove_permission_from_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    permission_id: int,
    current_user: User = Depends(deps.check_permissions(action="update", resource_type="role")),
) -> Any:
    """
    Remove a permission from a role.
    """
    return role_service.remove_permission(db, role_id=role_id, permission_id=permission_id)


@router.post("/{role_id}/users/{user_id}")
def add_user_to_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    user_id: int,
    current_user: User = Depends(deps.check_permissions(action="update", resource_type="role")),
) -> Any:
    """
    Add a user to a role.
    """
    return role_service.add_user(db, role_id=role_id, user_id=user_id)


@router.delete("/{role_id}/users/{user_id}")
def remove_user_from_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    user_id: int,
    current_user: User = Depends(deps.check_permissions(action="update", resource_type="role")),
) -> Any:
    """
    Remove a user from a role.
    """
    return role_service.remove_user(db, role_id=role_id, user_id=user_id) 