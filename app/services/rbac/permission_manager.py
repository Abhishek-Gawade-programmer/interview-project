from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.permission import Permission


def create_default_permissions(db: Session) -> None:
    """
    Create default roles and permissions.
    """
    # Create default roles if they don't exist
    roles = {
        "admin": "Administrator with full access",
        "user": "Regular user with limited access",
        "guest": "Guest user with minimal access",
    }

    for role_name, description in roles.items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=description)
            db.add(role)

    db.commit()

    # Create default permissions if they don't exist
    permissions = [
        # User permissions
        {
            "name": "user:read",
            "resource": "user",
            "action": "read",
            "description": "Read user information",
        },
        {
            "name": "user:create",
            "resource": "user",
            "action": "create",
            "description": "Create users",
        },
        {
            "name": "user:update",
            "resource": "user",
            "action": "update",
            "description": "Update user information",
        },
        {
            "name": "user:delete",
            "resource": "user",
            "action": "delete",
            "description": "Delete users",
        },
        # Role permissions
        {
            "name": "role:read",
            "resource": "role",
            "action": "read",
            "description": "Read role information",
        },
        {
            "name": "role:create",
            "resource": "role",
            "action": "create",
            "description": "Create roles",
        },
        {
            "name": "role:update",
            "resource": "role",
            "action": "update",
            "description": "Update role information",
        },
        {
            "name": "role:delete",
            "resource": "role",
            "action": "delete",
            "description": "Delete roles",
        },
        # Document permissions
        {
            "name": "document:read",
            "resource": "document",
            "action": "read",
            "description": "Read documents",
        },
        {
            "name": "document:create",
            "resource": "document",
            "action": "create",
            "description": "Create documents",
        },
        {
            "name": "document:update",
            "resource": "document",
            "action": "update",
            "description": "Update documents",
        },
        {
            "name": "document:delete",
            "resource": "document",
            "action": "delete",
            "description": "Delete documents",
        },
    ]

    for perm_data in permissions:
        perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not perm:
            perm = Permission(**perm_data)
            db.add(perm)

    db.commit()

    # Assign permissions to roles
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    user_role = db.query(Role).filter(Role.name == "user").first()
    guest_role = db.query(Role).filter(Role.name == "guest").first()

    # Admin gets all permissions
    all_permissions = db.query(Permission).all()
    admin_role.permissions = all_permissions

    # User gets basic permissions
    user_permissions = (
        db.query(Permission)
        .filter(
            Permission.name.in_(
                [
                    "user:read",
                    "document:read",
                    "document:create",
                    "document:update",
                    "document:delete",
                ]
            )
        )
        .all()
    )
    user_role.permissions = user_permissions

    # Guest gets minimal permissions
    guest_permissions = (
        db.query(Permission)
        .filter(
            Permission.name.in_(
                [
                    "user:read",
                    "document:read",
                ]
            )
        )
        .all()
    )
    guest_role.permissions = guest_permissions

    db.add_all([admin_role, user_role, guest_role])
    db.commit()
