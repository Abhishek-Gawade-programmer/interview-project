from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
import json

from app.db.session import get_db
from app.models.query import Query
from app.models.document import Document
from app.schemas.query import Query as QuerySchema, QueryCreate
from app.core.auth.dependencies import User, get_current_active_user

router = APIRouter()


@router.post("/", response_model=QuerySchema)
async def create_query(
    *,
    db: Session = Depends(get_db),
    query_in: QueryCreate = Body(...),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new query and generate a response using RAG.
    """
    # Check if document exists and user has access to it
    if query_in.document_id:
        document = db.query(Document).filter(Document.id == query_in.document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if document.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions to access this document")
        
        if not document.embedding_status:
            raise HTTPException(
                status_code=400,
                detail="Document has not been processed yet. Please process the document first."
            )
    
    # Create the query
    query = Query(
        query_text=query_in.query_text,
        user_id=current_user.id,
        document_id=query_in.document_id,
        response="Processing..."  # Initial response while we process
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    
    try:
        # Import embedding manager
        from app.rag.embeddings import embedding_manager
        
        if query_in.document_id:
            # Use embedding manager to search for relevant chunks
            search_results = embedding_manager.search_similar_chunks(
                query=query_in.query_text,
                document_id=query_in.document_id,
                top_k=3
            )
            
            # Build context from search results
            context = "\n\n".join([result["content"] for result in search_results])
            
            # Simulate a response based on the context (in a real app, we'd use an LLM here)
            response = f"Based on the document, I can provide this information:\n\n"
            response += f"The document contains information about {document.title}.\n"
            response += f"Here's a summary based on the document content: This is a simulated response that would normally be generated by an LLM using the context from the document."
            
            # You could also include top chunks in the response for debugging
            response += f"\n\nTop relevant chunks:\n"
            for i, result in enumerate(search_results):
                response += f"\n{i+1}. {result['content'][:100]}... (score: {result['score']:.2f})"
        else:
            # General query without document context
            response = f"You asked: {query_in.query_text}\n\n"
            response += "This is a simulated response that would normally be generated by an LLM."
        
        # Update the query with the response
        query.response = response
        db.add(query)
        db.commit()
        db.refresh(query)
        
        return query
    except Exception as e:
        # Update with error message
        query.response = f"Error generating response: {str(e)}"
        db.add(query)
        db.commit()
        
        # Re-raise for API response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}",
        )


@router.get("/", response_model=List[QuerySchema])
async def read_queries(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    document_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve queries created by the current user.
    """
    query = db.query(Query).filter(Query.user_id == current_user.id)
    
    if document_id:
        query = query.filter(Query.document_id == document_id)
    
    queries = query.offset(skip).limit(limit).all()
    return queries


@router.get("/{query_id}", response_model=QuerySchema)
async def read_query(
    query_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific query by ID.
    """
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    # Check if user owns the query
    if query.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return query 