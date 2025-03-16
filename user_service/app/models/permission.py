from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.role import role_permission

class Permission(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    resource = Column(String, nullable=False)  # The resource this permission applies to
    action = Column(String, nullable=False)    # The action allowed (read, write, delete, etc.)
    
    # Relationships
    roles = relationship("Role", secondary=role_permission, back_populates="permissions") 