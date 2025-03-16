from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, users, documents, roles
from app.core.config import settings
from app.db.init_db import create_first_admin

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="FastAPI microservice with AI integration and RBAC",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(documents.router, prefix=settings.API_V1_STR, tags=["documents"])
app.include_router(roles.router, prefix=settings.API_V1_STR, tags=["roles"])


@app.on_event("startup")
async def startup_event():
    # Create admin user on startup if it doesn't exist
    create_first_admin()


@app.get("/", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Service is running"}


# Health check endpoint for Railway deployment
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
