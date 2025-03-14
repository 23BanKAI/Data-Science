from confluent_kafka import Producer
import json

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "user_created"

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

def publish_user_created_event(username: str):
    """Публикует событие создания пользователя в Kafka"""
    event = {"username": username}
    producer.produce(KAFKA_TOPIC, key=username, value=json.dumps(event))
    producer.flush()
