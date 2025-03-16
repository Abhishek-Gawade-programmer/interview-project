from typing import Optional
from sqlalchemy.orm import Session
from oso import Oso

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


# Initialize Oso
oso = Oso()


def initialize_oso():
    """
    Initialize Oso with our authorization rules.
    """
    # Register classes
    oso.register_class(User)
    oso.register_class(Role)
    oso.register_class(Permission)

    # Load policy from string (in a real app, you might load from a file)
    oso.load_str(
        """
    # Define User as an actor for our policy
    actor User {}
    
    # Define resources
    resource String {}
    
    # Allow superusers to do anything
    allow(user: User, _action, _resource) if user.is_superuser;
    
    # Allow users to perform actions based on their role's permissions
    allow(user: User, action: String, resource: String) if
        has_permission(user, resource, action);
    
    # Helper rule to check if a user has a permission
    has_permission(user: User, resource: String, action: String) if
        user.role and
        permission in user.role.permissions and
        permission.resource = resource and
        permission.action = action;
    """
    )


# Initialize Oso on module import
initialize_oso()


def authorize(db: Session, user: User, resource: str, action: str) -> bool:
    """
    Check if a user is authorized to perform an action on a resource.
    """
    # Ensure user has role loaded
    if user.role is None and user.role_id is not None:
        user.role = db.query(Role).filter(Role.id == user.role_id).first()

    # Ensure role has permissions loaded
    if user.role and not user.role.permissions:
        role = (
            db.query(Role)
            .filter(Role.id == user.role.id)
            .options(db.joinedload(Role.permissions))
            .first()
        )
        if role:
            user.role.permissions = role.permissions

    # Check authorization
    return oso.is_allowed(user, action, resource)
