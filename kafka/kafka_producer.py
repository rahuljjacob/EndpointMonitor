# kafka_producer.py

# Import Kafka Producer from Confluent Kafka library
from confluent_kafka import Producer
import json
import os
from dotenv import load_dotenv  # To load environment variables from a .env file
import time

# Load environment variables from .env file (if it exists)
load_dotenv()

# Kafka configuration: Get the Kafka broker address and topic name from environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_LOG_TOPIC = os.getenv("KAFKA_LOG_TOPIC", "api-logs")

# Initialize the Kafka producer with the bootstrap servers
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

# This callback function is triggered once the message is delivered (or fails to deliver)
def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Function to send a log (as a dictionary) to the Kafka topic
def send_log_to_kafka(log_data: dict):
    try:
        # Convert dict to JSON string, encode to UTF-8, and produce the message to Kafka
        producer.produce(
            topic=KAFKA_LOG_TOPIC,
            value=json.dumps(log_data).encode("utf-8"),
            callback=delivery_report
        )
        
        # Let the producer process delivery reports (non-blocking)
        producer.poll(0)

        # Ensure all messages are sent (flush forces delivery)
        producer.flush()

        # Optional delay to simulate log batching or throttling
        time.sleep(1)
    except Exception as e:
        print(f"Error sending log to Kafka: {str(e)}")
