from confluent_kafka import Consumer
import psycopg2
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_LOG_TOPIC = os.getenv("KAFKA_LOG_TOPIC", "api-logs")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "log-consumer-group")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([KAFKA_LOG_TOPIC])

# Connect to PostgreSQL


def connect_db():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )


def store_log_in_db(log_data):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                path TEXT,
                method TEXT,
                endpoint TEXT,
                client_ip TEXT,
                timestamp TIMESTAMP,
                request_id TEXT,
                user_agent TEXT,
                status_code INT,
                response_time_ms FLOAT
            )
        """)
        conn.commit()

        cursor.execute("""
            INSERT INTO logs (path, method, endpoint, client_ip, timestamp, request_id, user_agent, status_code, response_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            log_data.get("path"),
            log_data.get("method"),
            log_data.get("endpoint"),
            log_data.get("client_ip"),
            log_data.get("timestamp"),
            log_data.get("request_id"),
            log_data.get("user_agent"),
            log_data.get("status_code"),
            log_data.get("response_time_ms"),
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")


print("Kafka Consumer Started...")
while True:
    msg = consumer.poll(1.0)  # Poll for messages
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    log_data = json.loads(msg.value().decode("utf-8"))
    print(f"Received log: {log_data}")
    store_log_in_db(log_data)
    print("Log stored in DB.")

consumer.close()
