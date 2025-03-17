# FastAPI Microservices: User Management & RAG Services

This project implements a microservices architecture consisting of two main services:

1. **User Service**: Handles user authentication, authorization, and RBAC (Role-Based Access Control)
2. **RAG Service**: Implements a Retrieval-Augmented Generation system for processing documents and answering queries

## Architecture Overview

The system is organized as follows:

```
fastapi-microservices/
├── user_service/             # User service implementation
│   ├── app/                  # Application code
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core functionality
│   │   ├── crud/             # Database operations
│   │   ├── db/               # Database setup
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic models
│   │   └── main.py           # Application entry point
│   └── Dockerfile            # User service container definition
├── rag_service/              # RAG service implementation
│   ├── app/                  # Application code
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core functionality
│   │   ├── crud/             # Database operations
│   │   ├── db/               # Database setup
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic models
│   │   └── main.py           # Application entry point
│   └── Dockerfile            # RAG service container definition
├── uploads/                  # Shared directory for document uploads
├── docker-compose.yml        # Services configuration
├── requirements.txt          # Project dependencies
├── init_db.py                # Database initialization script
└── QUICK_START.md            # Quick start guide for setup
```

## Features

### User Service

- User registration and authentication
- JWT token-based authentication
- Role-based access control (RBAC)
- User profile management
- Permission management

### RAG Service

- Document upload and storage
- Document processing (text extraction, chunking)
- Vector database integration for semantic search
- Query handling with AI-generated responses
- Access control integrated with User Service

## Technical Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: PostgreSQL, SQLAlchemy ORM
- **Authentication**: JWT tokens, OAuth2 with Password flow
- **Authorization**: Custom RBAC system
- **AI/NLP**: LangChain, OpenAI API
- **Vector Database**: ChromaDB
- **Containerization**: Docker, Docker Compose
- **API Documentation**: Swagger UI (via FastAPI)

## Getting Started

See the [QUICK_START.md](QUICK_START.md) file for detailed setup instructions.

## API Documentation

After starting the services, you can access the API documentation at:

- User Service: http://localhost:8000/docs
- RAG Service: http://localhost:8001/docs

## Testing

Each service includes unit and integration tests that can be run with pytest:

```bash
cd user_service
pytest

cd ../rag_service
pytest
```

## Security

This system implements several security measures:

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- Input validation with Pydantic
- Database query protection with SQLAlchemy


