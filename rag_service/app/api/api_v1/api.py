from fastapi import APIRouter

from app.api.api_v1.endpoints import documents, queries

api_router = APIRouter()
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(queries.router, prefix="/queries", tags=["queries"]) 