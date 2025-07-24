FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies with proper PostgreSQL client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    librdkafka-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements from root directory
COPY ../requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY /kafka/kafka_consumer.py .
COPY .env .

CMD ["python", "kafka_consumer.py"]