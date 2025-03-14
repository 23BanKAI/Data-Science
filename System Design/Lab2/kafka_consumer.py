from kafka import KafkaConsumer
import json
import os
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Order

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

def save_order_to_db(order_data, db: Session):
    new_order = Order(
        user_id=order_data["user_id"],
        service=order_data["service"],
        status=order_data["status"]
    )
    db.add(new_order)
    db.commit()

def consume_orders():
    db = SessionLocal()
    try:
        for message in consumer:
            order_data = message.value
            save_order_to_db(order_data, db)
    finally:
        db.close()

if __name__ == "__main__":
    consume_orders()
