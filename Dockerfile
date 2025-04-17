# Use official Python image with security updates
FROM python:3.11-slim-bookworm

# Set security-focused environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Create app directory and set up user first
RUN mkdir -p /app && \
    useradd -m appuser && \
    chown -R appuser:appuser /app

WORKDIR /app

# Install system dependencies with security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install spaCy English model
RUN pip install --no-cache-dir spacy && python -m spacy download en_core_web_sm

# Switch to non-root user
USER appuser

# Copy requirements first to leverage Docker cache
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser app1.py .

# Use production-grade server
EXPOSE 80
CMD ["streamlit", "run", "app1.py", "--server.port=80", "--server.address=0.0.0.0"]
