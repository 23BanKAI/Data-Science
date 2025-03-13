from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Order
from pydantic_models import OrderCreate, OrderResponse  # Импортируем Pydantic-модель
from auth import verify_jwt
from models import User, Order

router = APIRouter()

@router.post("/orders")
def create_order(order: OrderCreate, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    new_order = Order(user_id=order.user_id, service=order.service, status=order.status)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/list", response_model=list[OrderResponse])
def list_orders(username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    # Получаем пользователя по имени
    db_user = db.query(User).filter(User.username == username).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Получаем все заказы этого пользователя
    user_orders = db.query(Order).filter(Order.user_id == db_user.id).all()
    
    # Возвращаем заказы в формате, который соответствует OrderResponse
    return [OrderResponse(order_id=o.order_id, service=o.service, status=o.status) for o in user_orders]

@router.put("/update/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db), username: str = Depends(verify_jwt)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_order = db.query(Order).filter(Order.order_id == order_id, Order.user_id == db_user.id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Обновляем статус или услугу заказа
    if order_update.status:
        db_order.status = order_update.status
    if order_update.service:
        db_order.service = order_update.service

    db.commit()
    db.refresh(db_order)
    
    return OrderResponse(order_id=db_order.order_id, service=db_order.service, status=db_order.status)

@router.delete("/delete/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db), username: str = Depends(verify_jwt)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_order = db.query(Order).filter(Order.order_id == order_id, Order.user_id == db_user.id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    
    return {"message": f"Order {order_id} deleted successfully"}