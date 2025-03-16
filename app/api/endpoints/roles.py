from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_active_superuser
from app.api.dependencies.rbac import check_permission
from app.db.session import get_db
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.role import Role as RoleSchema, RoleCreate, RoleUpdate

router = APIRouter()


@router.get("/roles", response_model=List[RoleSchema])
def read_roles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(check_permission("role", "read")),
) -> Any:
    """
    Retrieve roles.
    """
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.post("/roles", response_model=RoleSchema)
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
    current_user: Any = Depends(check_permission("role", "create")),
) -> Any:
    """
    Create new role.
    """
    # Check if role with this name exists
    role = db.query(Role).filter(Role.name == role_in.name).first()
    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The role with this name already exists in the system.",
        )

    # Create new role
    role = Role(
        name=role_in.name,
        description=role_in.description,
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.get("/roles/{role_id}", response_model=RoleSchema)
def read_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: Any = Depends(check_permission("role", "read")),
) -> Any:
    """
    Get role by ID.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The role with this ID does not exist in the system",
        )
    return role


@router.put("/roles/{role_id}", response_model=RoleSchema)
def update_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: Any = Depends(check_permission("role", "update")),
) -> Any:
    """
    Update a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The role with this ID does not exist in the system",
        )

    # Update role
    if role_in.name is not None:
        # Check if name is already taken
        name_role = db.query(Role).filter(Role.name == role_in.name).first()
        if name_role and name_role.id != role_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The role with this name already exists in the system.",
            )
        role.name = role_in.name

    if role_in.description is not None:
        role.description = role_in.description

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.delete("/roles/{role_id}", response_model=RoleSchema)
def delete_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: Any = Depends(check_permission("role", "delete")),
) -> Any:
    """
    Delete a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The role with this ID does not exist in the system",
        )

    db.delete(role)
    db.commit()
    return role


@router.post("/roles/{role_id}/permissions/{permission_id}", response_model=RoleSchema)
def add_permission_to_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    permission_id: int,
    current_user: Any = Depends(check_permission("role", "update")),
) -> Any:
    """
    Add a permission to a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The role with this ID does not exist in the system",
        )

    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The permission with this ID does not exist in the system",
        )

    # Check if permission is already assigned to role
    if permission in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The permission is already assigned to this role",
        )

    # Add permission to role
    role.permissions.append(permission)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.delete(
    "/roles/{role_id}/permissions/{permission_id}", response_model=RoleSchema
)
def remove_permission_from_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    permission_id: int,
    current_user: Any = Depends(check_permission("role", "update")),
) -> Any:
    """
    Remove a permission from a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The role with this ID does not exist in the system",
        )

    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The permission with this ID does not exist in the system",
        )

    # Check if permission is assigned to role
    if permission not in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The permission is not assigned to this role",
        )

    # Remove permission from role
    role.permissions.remove(permission)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role
