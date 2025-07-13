# 🧠 Kafka Logging Middleware (FastAPI)

A minimal FastAPI app that logs API requests (and errors) to **Apache Kafka** using a custom middleware.

## 🎯 Features

- Intercepts and logs requests/responses using Starlette middleware
- Sends structured logs to Kafka using `confluent_kafka`
- Observes logs via a Kafka consumer
- Tests various request types and error conditions

## 📦 Requirements

- Python 3.8+
- Docker and Docker Compose
- FastAPI and its dependencies
- Apache Kafka

## 🗂️ Project Structure

```plaintext
api-server/
├── main.py                 # FastAPI application
├── middlewares/
│   ├── __init__.py
│   └── logging_middleware.py   # Logging middleware
├── kafka/
│   └── kafka_producer.py   # Kafka producer logic
├── test_producer.py        # Manual log sender
├── test_consumer.py        # Kafka log listener
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker services configuration
└── README.md              # Project documentation
```

## 🚀 Getting Started

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone <repository-url>
   cd api-server
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start Kafka and Zookeeper services:

   ```bash
   docker-compose up -d
   ```

4. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

5. (Optional) Start the Kafka consumer to monitor logs:
   ```bash
   python test_consumer.py
   ```

## 🔍 API Endpoints

| Endpoint           | Method | Description                 |
| ------------------ | ------ | --------------------------- |
| `/ping`            | GET    | Health check endpoint       |
| `/users/{user_id}` | GET    | Get user details by ID      |
| `/submit`          | POST   | Submit data with validation |
| `/error`           | GET    | Test error logging          |

### Example API Requests

#### Health Check

```bash
curl http://localhost:8000/ping
```

#### Submit Data

```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{"title": "Kafka Magic", "content": "Logging is awesome!"}'
```

## 🔧 Configuration

The application uses Docker Compose to set up Kafka and Zookeeper with the following configurations:

- Zookeeper: Port 2181
- Kafka: Port 9092

## 🧪 Testing

Use `test_producer.py` to manually send test log messages with different severity levels:

```bash
python test_producer.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
