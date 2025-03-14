from fastapi import APIRouter, Depends, HTTPException
from pydantic_models import OrderCreate, OrderResponse
from mongodb import create_order, get_orders_by_user, update_order, delete_order
from auth import verify_jwt
from models import User
from sqlalchemy.orm import Session
from database import SessionLocal
from redis_client import cache_orders, get_cached_orders, invalidate_cache

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders")
def create_order_route(order: OrderCreate, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_id = create_order(order)
    
    # Очистка кэша заказов пользователя, чтобы загрузить актуальные данные в следующий запрос
    invalidate_cache(user.id)

    return {"order_id": order_id}

@router.get("/list", response_model=list[OrderResponse])
def list_orders(username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверяем кэш
    cached_orders = get_cached_orders(user.id)
    if cached_orders:
        return cached_orders

    # Загружаем из MongoDB, если кэша нет
    orders = get_orders_by_user(user.id)

    # Кэшируем результат
    cache_orders(user.id, orders)

    return orders

@router.put("/update/{order_id}", response_model=OrderResponse)
def update_order_route(order_id: str, order_update: OrderCreate, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_order(order_id, order_update)

    # Очистка кэша
    invalidate_cache(user.id)

    return {"order_id": order_id, "service": order_update.service, "status": order_update.status}

@router.delete("/delete/{order_id}", response_model=dict)
def delete_order_route(order_id: str, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_order(order_id)

    # Очистка кэша
    invalidate_cache(user.id)

    return {"message": "Order deleted"}
