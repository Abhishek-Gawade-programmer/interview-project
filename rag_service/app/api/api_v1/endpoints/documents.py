from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import Document as DocumentSchema, DocumentCreate
from app.core.auth.dependencies import User, get_current_active_user, check_user_permission
from app.rag.document_processor import document_processor

router = APIRouter()


@router.get("/", response_model=List[DocumentSchema])
async def read_documents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve documents owned by the current user.
    """
    documents = db.query(Document).filter(Document.user_id == current_user.id).offset(skip).limit(limit).all()
    return documents


@router.post("/", response_model=DocumentSchema)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a new document.
    """
    try:
        # Detect file type
        file_type = document_processor.detect_file_type(file.filename)
        
        # Save the file
        file_path = document_processor.save_uploaded_file(file, current_user.id)
        
        # Create document in DB
        document_in = DocumentCreate(
            title=title,
            file_type=file_type,
            user_id=current_user.id
        )
        
        document = Document(
            title=document_in.title,
            file_type=document_in.file_type,
            file_path=file_path,
            user_id=document_in.user_id,
            embedding_status=False,
            content=None
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return document
    except Exception as e:
        # Clean up file if operation failed
        if "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}",
        )


@router.get("/{document_id}", response_model=DocumentSchema)
async def read_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific document by ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if user owns the document
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a document.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if user owns the document
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Delete the file
    if document.file_path and os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"status": "success", "message": "Document deleted successfully"}


@router.post("/{document_id}/process")
async def process_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Process a document (extract text, create chunks, generate embeddings).
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if user owns the document
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        # Extract text
        if not document.content:
            document.content = document_processor.load_document(document.file_path, document.file_type)
            db.add(document)
            db.commit()
            db.refresh(document)
        
        # Create chunks
        chunks = document_processor.split_text_into_chunks(document.content)
        
        # For now, we'll just create chunks in the database without embeddings
        # In a real implementation, you would generate embeddings and store them in a vector DB
        from app.models.chunk import Chunk
        for chunk_text in chunks:
            chunk = Chunk(
                content=chunk_text,
                document_id=document.id,
                embedding_id=None  # Would normally store the ID in the vector DB
            )
            db.add(chunk)
        
        # Update document status
        document.embedding_status = True
        db.add(document)
        db.commit()
        
        return {"status": "success", "message": "Document processed successfully", "chunks_count": len(chunks)}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}",
        ) 