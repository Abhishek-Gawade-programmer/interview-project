import os
import shutil
from typing import Any, List
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.rbac import check_permission
from app.db.session import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import (
    Document as DocumentSchema,
    DocumentCreate,
    DocumentQuery,
)
from app.services.ai.rag_pipeline import process_document, query_document

router = APIRouter()


@router.get("/documents", response_model=List[DocumentSchema])
def read_documents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve documents.
    """
    # If user is superuser, return all documents
    if current_user.is_superuser:
        documents = db.query(Document).offset(skip).limit(limit).all()
    else:
        # Otherwise, return only user's documents
        documents = (
            db.query(Document)
            .filter(Document.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return documents


@router.post("/documents", response_model=DocumentSchema)
async def create_document(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(check_permission("document", "create")),
) -> Any:
    """
    Create new document.
    """
    # Create directory for documents if it doesn't exist
    documents_dir = Path("documents")
    documents_dir.mkdir(exist_ok=True)

    # Create directory for user's documents if it doesn't exist
    user_documents_dir = documents_dir / str(current_user.id)
    user_documents_dir.mkdir(exist_ok=True)

    # Save file
    file_path = user_documents_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create document in database
    document = Document(
        name=file.filename,
        content_type=file.content_type,
        file_path=str(file_path),
        owner_id=current_user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # Process document for RAG
    try:
        vector_store_path = await process_document(document.id, str(file_path))
        document.vector_store_path = vector_store_path
        db.add(document)
        db.commit()
        db.refresh(document)
    except Exception as e:
        # If processing fails, delete document and file
        db.delete(document)
        db.commit()
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}",
        )

    return document


@router.get("/documents/{document_id}", response_model=DocumentSchema)
def read_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get document by ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The document with this ID does not exist in the system",
        )

    # Check if user is owner or superuser
    if document.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this document",
        )

    return document


@router.delete("/documents/{document_id}", response_model=DocumentSchema)
def delete_document(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    current_user: User = Depends(check_permission("document", "delete")),
) -> Any:
    """
    Delete a document.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The document with this ID does not exist in the system",
        )

    # Check if user is owner or superuser
    if document.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this document",
        )

    # Delete file
    try:
        os.remove(document.file_path)
    except Exception:
        pass

    # Delete vector store if it exists
    if document.vector_store_path:
        try:
            shutil.rmtree(document.vector_store_path)
        except Exception:
            pass

    # Delete document from database
    db.delete(document)
    db.commit()
    return document


@router.post("/documents/{document_id}/query")
async def query_document_endpoint(
    *,
    db: Session = Depends(get_db),
    document_id: int,
    query: DocumentQuery,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Query a document using RAG.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The document with this ID does not exist in the system",
        )

    # Check if user is owner or superuser
    if document.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to query this document",
        )

    # Check if document has been processed
    if not document.vector_store_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This document has not been processed for RAG yet",
        )

    # Query document
    try:
        result = await query_document(document.vector_store_path, query.query)
        return {"query": query.query, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query document: {str(e)}",
        )
