from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class with allow_unmapped enabled for SQLAlchemy 2.0 compatibility
Base = declarative_base()
Base.__allow_unmapped__ = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
