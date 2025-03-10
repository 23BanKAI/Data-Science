from fastapi import APIRouter, Depends, HTTPException
from models import Order
from database import orders_db
from auth import verify_jwt

router = APIRouter()

@router.post("/create")
def create_order(order: Order, username: str = Depends(verify_jwt)):
    order.order_id = len(orders_db) + 1
    order.user = username
    orders_db.append(order)
    return {"message": "Заказ создан", "order_id": order.order_id}

@router.get("/list")
def list_orders(username: str = Depends(verify_jwt)):
    user_orders = [order for order in orders_db if order.user == username]
    return user_orders
