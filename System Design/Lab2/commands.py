from sqlalchemy.orm import Session
from models import User
from pydantic_models import UserCreate
import bcrypt
from fastapi import HTTPException
from kafka_producer import publish_user_created_event


def register_user(user: UserCreate, db: Session):
    """Создание нового пользователя с отправкой события в Kafka"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Публикуем событие в Kafka
    publish_user_created_event(new_user.username)

    return new_user

def update_user_password(username: str, new_password: str, db: Session):
    """Обновление пароля пользователя"""
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(username: str, db: Session):
    """Удаление пользователя"""
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
