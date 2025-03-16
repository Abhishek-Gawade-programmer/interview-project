# Use Python 3.12 as base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create vector_stores directory
RUN mkdir -p vector_stores && chmod 777 vector_stores

# Create SQLite database directory if needed
RUN mkdir -p data && chmod 777 data

# Run migrations on startup
# Create an entrypoint script
RUN echo '#!/bin/sh\n\
    python -m alembic upgrade head\n\
    exec "$@"' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Start the application with Hypercorn
CMD ["hypercorn", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "2"] 