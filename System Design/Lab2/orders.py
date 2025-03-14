import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic_models import OrderCreate, OrderResponse
from mongodb import get_orders_by_user, update_order, delete_order
from auth import verify_jwt
from models import User
from sqlalchemy.orm import Session
from database import SessionLocal
from redis_client import redis_client
from kafka_producer import send_order_to_kafka

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CACHE_EXPIRATION = 300  # Время жизни кэша (5 минут)

# **Команда (Command): Отправка заказа в Kafka**
@router.post("/orders")
def create_order_route(order: OrderCreate, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_data = {
        "user_id": user.id,
        "service": order.service,
        "status": order.status,
    }

    send_order_to_kafka(order_data)

    return {"message": "Order is being processed"}

# **Запрос (Query): Получение списка заказов (из Redis или базы)**
@router.get("/orders", response_model=list[OrderResponse])
def list_orders(username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cache_key = f"orders:{user.id}"
    cached_orders = redis_client.get(cache_key)

    if cached_orders:
        return json.loads(cached_orders)

    orders = get_orders_by_user(user.id)

    redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps([order.dict() for order in orders]))

    return orders

# **Обновление заказа и очистка кеша**
@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order_route(order_id: str, order_update: OrderCreate, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_order(order_id, order_update)

    redis_client.delete(f"orders:{user.id}")

    return {"order_id": order_id, "service": order_update.service, "status": order_update.status}

# **Удаление заказа и очистка кеша**
@router.delete("/orders/{order_id}", response_model=dict)
def delete_order_route(order_id: str, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_order(order_id)

    redis_client.delete(f"orders:{user.id}")

    return {"message": f"Order {order_id} deleted successfully"}
