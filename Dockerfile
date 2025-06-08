# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY Psocial/ .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run migrations and start Gunicorn (for production)
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 psocial.wsgi:application"]