# Base image
FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

ENV API_URL="https://toolbox-service-99546327658.us-central1.run.app"
ENV TARGET_SA="way-back-home-sa@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com"
ENV AUDIENCE="jobs-agent"

#ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/adc.json

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Cloud Run uses PORT env variable
ENV PORT=8080

# Expose container port
EXPOSE 8080

# Start FastAPI app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]