from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Document(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    file_path = Column(String)
    file_type = Column(String)
    embedding_status = Column(Boolean, default=False)
    user_id = Column(Integer, index=True)  # Store the user ID from the user service
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship with chunks
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan") 