FROM python:3.12

WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the upload directory
RUN mkdir -p /app/uploads

# Copy the service code
COPY ./rag_service ./

# Expose the port
EXPOSE 8000

# Run the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
