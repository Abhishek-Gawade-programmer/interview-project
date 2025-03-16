from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import BaseModel
from app.models.role import role_permission


class Permission(BaseModel):
    """
    Permission model for RBAC.
    """

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    resource = Column(
        String, nullable=False
    )  # Resource name (e.g., "user", "document")
    action = Column(
        String, nullable=False
    )  # Action name (e.g., "read", "write", "delete")

    # Relationships
    roles = relationship(
        "Role", secondary=role_permission, back_populates="permissions"
    )
