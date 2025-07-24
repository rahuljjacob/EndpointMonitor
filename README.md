# monitorize: Application Monitoring Dashboard

Monitorize is a containerized, real-time API monitoring and logging system built with FastAPI, Kafka, PostgreSQL, and Grafana. It logs every API request, stores logs in a database, and visualizes them with Grafana dashboards. The system is orchestrated using Docker Compose for easy deployment.

## Architecture

```
[Client/Simulator]
      |
      v
 [FastAPI App] --(logs)--> [Kafka] --(logs)--> [Kafka Consumer] --(logs)--> [PostgreSQL]
      |                                                           |
      |                                                           v
      |                                                      [Grafana]
      |
      v
[simulate_requests.py]
```

- **FastAPI**: Handles API requests and logs them via middleware.
- **Kafka**: Message broker for log entries.
- **Kafka Consumer**: Reads logs from Kafka and writes to PostgreSQL.
- **PostgreSQL**: Stores all API logs.
- **Grafana**: Visualizes logs and metrics from PostgreSQL.
- **simulate_requests.py**: Generates test traffic for the API.

## Features

- Real-time logging of all API requests (method, endpoint, status, response time, client IP, etc.)
- Log transport via Kafka for scalability
- Persistent storage of logs in PostgreSQL
- Grafana dashboard for visualization
- Fully containerized with Docker Compose

## Setup & Usage

### Prerequisites

- Docker & Docker Compose installed
- Python 3.9+

### Environment Variables

Create a `.env` file in the project root with the following (example):

```
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=logsdb
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=adminpass
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
```

### Running the System

```bash
docker-compose up --build
```

- FastAPI app: [http://localhost:8000](http://localhost:8000)
- Grafana: [http://localhost:3000](http://localhost:3000)
- pgAdmin: [http://localhost:5050](http://localhost:5050)

### Simulating Requests

In a separate terminal, run:

```bash
python simulate_requests.py
```

This will continuously send GET and POST requests to the FastAPI app, generating logs and errors for demo purposes.

## File Structure

- `main.py` — FastAPI app with logging middleware
- `simulate_requests.py` — Request generator for testing
- `kafka/kafka_producer.py` — Sends logs to Kafka
- `kafka/kafka_consumer.py` — Consumes logs and writes to PostgreSQL
- `grafana/dashboard.json` — Grafana dashboard config
- `docker-compose.yml` — Orchestrates all services
- `Dockerfile.fastapi` — FastAPI app container
- `kafka/Dockerfile` — Kafka consumer container
- `requirements.txt` — Python dependencies for FastAPI app
- `kafka/requirements.txt` — Python dependencies for Kafka consumer

## Endpoints (FastAPI)

- `GET /` — Home page
- `GET /ping` — Health check
- `GET /users/{user_id}` — Get user info (positive integers only)
- `POST /submit` — Submit data (requires `title` and `content`)
- `GET /error` — Simulate an error (for testing)
- `GET /version` — API version info
- `GET /status` — System status

## Technologies Used

- **FastAPI** (Python web framework)
- **Kafka** (message broker)
- **PostgreSQL** (database)
- **Grafana** (visualization)
- **Docker Compose** (orchestration)
- **pgAdmin** (PostgreSQL admin UI)

