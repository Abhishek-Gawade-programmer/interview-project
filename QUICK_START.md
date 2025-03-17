# Quick Start Guide

This guide will help you get up and running with the FastAPI microservices project quickly.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ (for local development)
- PostgreSQL (for local development without Docker)

## Option 1: Running with Docker Compose (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fastapi-microservices.git
   cd fastapi-microservices
   ```

2. Start all services:

   ```bash
   docker-compose up -d
   ```

3. Initialize the databases:

   ```bash
   docker-compose exec user-service python -m init_db
   ```

4. Access the services:

   - User Service: http://localhost:8000/docs
   - RAG Service: http://localhost:8001/docs

5. Login with default credentials:
   - Admin user: `admin@example.com` / `admin`
   - Regular user: `user@example.com` / `user`

## Option 2: Local Development

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fastapi-microservices.git
   cd fastapi-microservices
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL databases:

   ```bash
   createdb user_service
   createdb rag_service
   ```

5. Initialize the databases:

   ```bash
   python init_db.py
   ```

6. Start the User Service (in terminal 1):

   ```bash
   cd user_service
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

7. Start the RAG Service (in terminal 2):

   ```bash
   cd rag_service
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

8. Access the services:
   - User Service: http://localhost:8000/docs
   - RAG Service: http://localhost:8001/docs

## Example Workflow

1. Login to get an access token
2. Upload a document to the RAG service
3. Process the document to extract text and create chunks
4. Query the document to get AI-generated responses

### Example Using Curl

1. Get an access token:

   ```bash
   curl -X 'POST' \
     'http://localhost:8000/api/v1/auth/login' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=admin%40example.com&password=admin'
   ```

2. Upload a document (replace `YOUR_TOKEN` with the token from step 1):

   ```bash
   curl -X 'POST' \
     'http://localhost:8001/api/v1/documents/' \
     -H 'accept: application/json' \
     -H 'Authorization: Bearer YOUR_TOKEN' \
     -H 'Content-Type: multipart/form-data' \
     -F 'file=@/path/to/your/document.txt' \
     -F 'title=My Document'
   ```

3. Process the document (replace `YOUR_TOKEN` and `DOCUMENT_ID`):

   ```bash
   curl -X 'POST' \
     'http://localhost:8001/api/v1/documents/DOCUMENT_ID/process' \
     -H 'accept: application/json' \
     -H 'Authorization: Bearer YOUR_TOKEN'
   ```

4. Query the document (replace `YOUR_TOKEN` and `DOCUMENT_ID`):
   ```bash
   curl -X 'POST' \
     'http://localhost:8001/api/v1/queries/' \
     -H 'accept: application/json' \
     -H 'Authorization: Bearer YOUR_TOKEN' \
     -H 'Content-Type: application/json' \
     -d '{
       "query_text": "What is this document about?",
       "document_id": DOCUMENT_ID
     }'
   ```

## Troubleshooting

- If you encounter database connection issues, ensure PostgreSQL is running and the connection details are correct.
- For authorization issues, check that you're using the correct token and that it hasn't expired.
- If the RAG service can't connect to the User service, ensure both services are running and can communicate with each other.
