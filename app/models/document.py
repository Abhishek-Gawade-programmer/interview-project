from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import BaseModel


class Document(BaseModel):
    """
    Document model for storing uploaded documents for RAG.
    """

    name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content = Column(
        Text, nullable=True
    )  # Optional: Store document content for small documents
    vector_store_path = Column(
        String, nullable=True
    )  # Path to the vector store for this document

    # Relationship with User
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="documents")
