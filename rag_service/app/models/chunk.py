from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Chunk(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    embedding_id = Column(String, index=True)
    document_id = Column(Integer, ForeignKey("document.id"))
    
    # Relationship with document
    document = relationship("Document", back_populates="chunks") 