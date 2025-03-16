# FastAPI Microservice with AI Integration and RBAC

This project is a FastAPI microservice that includes:

- CRUD operations for user profile management
- JWT-based authentication & authorization
- A RAG pipeline for processing and querying large text documents using AI
- Dynamic Role-Based Access Control (RBAC) using the Oso framework

## Project Structure

```
app/
├── api/                  # API routes and dependencies
│   ├── endpoints/        # API endpoints
│   └── dependencies/     # API dependencies
├── core/                 # Core application modules
│   └── security/         # Security modules
├── db/                   # Database modules
├── models/               # SQLAlchemy models
├── schemas/              # Pydantic schemas
├── services/             # Service modules
│   ├── ai/               # AI service modules
│   └── rbac/             # RBAC service modules
├── utils/                # Utility modules
└── tests/                # Test modules
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your configuration

### Database Setup

```bash
alembic upgrade head
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the Swagger UI at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## API Usage

### Authentication

1. Register a new user:

```bash
curl -X POST "http://localhost:8000/api/users" -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "strongpassword", "username": "user"}'
```

2. Login and get an access token:

```bash
curl -X POST "http://localhost:8000/api/login" -H "Content-Type: application/json" -d '{"username": "user@example.com", "password": "strongpassword"}'
```

### User Profile

1. Get user profile (requires authentication):

```bash
curl -X GET "http://localhost:8000/api/users/me" -H "Authorization: Bearer {your_access_token}"
```

### Document Processing

1. Upload a document (requires authentication):

```bash
curl -X POST "http://localhost:8000/api/documents" -H "Authorization: Bearer {your_access_token}" -F "file=@document.pdf"
```

2. Query a document (requires authentication):

```bash
curl -X POST "http://localhost:8000/api/documents/{document_id}/query" -H "Authorization: Bearer {your_access_token}" -H "Content-Type: application/json" -d '{"query": "What is the main topic of this document?"}'
```

## Testing

Run the tests using pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
