from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic_models import UserCreate, UserResponse
from database import get_db
import jwt
import datetime
from auth import verify_jwt
from commands import register_user, update_user_password, delete_user
from queries import get_user_by_username

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def create_jwt(username: str):
    """Создает JWT токен"""
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Регистрация пользователя"""
    new_user = register_user(user, db)
    token = create_jwt(new_user.username)
    return UserResponse(username=new_user.username, token=token)

@router.put("/update", response_model=UserResponse)
def update_user(user_update: UserCreate, db: Session = Depends(get_db), username: str = Depends(verify_jwt)):
    """Обновление пароля пользователя"""
    updated_user = update_user_password(username, user_update.password, db)
    return UserResponse(username=updated_user.username, token=create_jwt(updated_user.username))

@router.get("/me", response_model=UserResponse)
def get_current_user(db: Session = Depends(get_db), username: str = Depends(verify_jwt)):
    """Получение информации о текущем пользователе"""
    user = get_user_by_username(username, db)
    return UserResponse(username=user.username, token=create_jwt(user.username))

@router.delete("/delete", response_model=dict)
def remove_user(db: Session = Depends(get_db), username: str = Depends(verify_jwt)):
    """Удаление пользователя"""
    delete_user(username, db)
    return {"message": f"User {username} deleted successfully"}
