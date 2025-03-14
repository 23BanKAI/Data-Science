from sqlalchemy.orm import Session
from models import User
from fastapi import HTTPException

def get_user_by_username(username: str, db: Session):
    """Получение пользователя по username"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user