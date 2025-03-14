from confluent_kafka import Consumer
import json
from database import SessionLocal
from models import User

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "user_created"
KAFKA_GROUP_ID = "user_service"

consumer = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": KAFKA_GROUP_ID,
    "auto.offset.reset": "earliest"
})

def consume_messages():
    """Читает сообщения из Kafka и записывает пользователей в БД"""
    consumer.subscribe([KAFKA_TOPIC])

    while True:
        msg = consumer.poll(1.0)  # Ожидание сообщения
        if msg is None:
            continue
        if msg.error():
            print(f"Ошибка Kafka: {msg.error()}")
            continue

        try:
            event = json.loads(msg.value().decode("utf-8"))
            username = event["username"]

            # Записываем в БД
            db = SessionLocal()
            new_user = User(username=username, password="")  # Пароль пустой, т.к. он есть в основном сервисе
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.close()

            print(f"Добавлен пользователь {username} в БД")
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")

if __name__ == "__main__":
    consume_messages()
