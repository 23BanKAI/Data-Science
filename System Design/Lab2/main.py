from fastapi import FastAPI
from users import router as users_router
from database import engine, Base
from auth import create_superuser, auth_router 
from orders import router as orders_router
from auth import verify_jwt
from pydantic_models import UserCreate, UserResponse
from models import User
from database import get_db
import bcrypt
import jwt
import datetime

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    pass

# Подключение маршрутов
app.include_router(users_router, prefix="/users", tags=["Пользователи"])
app.include_router(orders_router, prefix="/orders", tags=["Заказы"])
app.include_router(auth_router, prefix="/auth", tags=["Авторизация"])

@app.get("/")
def root():
    return {"message": "Система заказа услуг работает!"}
