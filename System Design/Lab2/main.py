from fastapi import FastAPI
import users
from auth import create_superuser
import orders

app = FastAPI(title="Сервис заказов")

@app.on_event("startup")
async def on_startup():
    # Создание суперпользователя
    await create_superuser()

# Подключаем маршруты
app.include_router(users.router, prefix="/users", tags=["Пользователи"])
app.include_router(orders.router, prefix="/orders", tags=["Заказы"])

@app.get("/")
def root():
    return {"message": "Система заказа услуг работает!"}    