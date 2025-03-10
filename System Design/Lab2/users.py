from fastapi import APIRouter, HTTPException
from models import User, UserResponse
from auth import create_jwt
from database import users_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    users_db[user.username] = user
    token = create_jwt(user.username)
    return {"username": user.username, "token": token}

@router.post("/login", response_model=UserResponse)
def login(user: User):
    if user.username not in users_db or users_db[user.username].password != user.password:
        raise HTTPException(status_code=400, detail="Неверные учетные данные")
    
    token = create_jwt(user.username)
    return {"username": user.username, "token": token}
