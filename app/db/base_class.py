from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
import inflect

p = inflect.engine()

# Create a declarative base class with allow_unmapped enabled
Base = declarative_base()
Base.__allow_unmapped__ = True


# Add default columns and __tablename__ generator
class BaseModel(Base):
    """Base model class for all tables"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(cls) -> str:
        return p.plural(cls.__name__.lower())
