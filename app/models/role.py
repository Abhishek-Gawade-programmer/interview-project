from sqlalchemy import Column, String, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base, BaseModel

# Association table for many-to-many relationship between roles and permissions
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)


class Role(BaseModel):
    """
    Role model for RBAC.
    """

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Relationships
    users = relationship("User", back_populates="role")
    permissions = relationship(
        "Permission", secondary=role_permission, back_populates="roles"
    )
