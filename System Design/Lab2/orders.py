from fastapi import APIRouter, Depends, HTTPException
from pydantic_models import OrderCreate, OrderResponse
from mongodb import create_order, get_orders_by_user, update_order, delete_order
from auth import verify_jwt
from models import User
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders")
def create_order_route(order: OrderCreate, username: str = Depends(verify_jwt), db: Session = Depends(get_db)) :
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_id = create_order(order)
    return {"order_id": order_id}

@router.get("/list", response_model=list[OrderResponse])
def list_orders(username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    orders = get_orders_by_user(user.id)
    return orders

@router.put("/update/{order_id}", response_model=OrderResponse)
def update_order_route(order_id: str, order_update: OrderCreate, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_order(order_id, order_update)
    return {"order_id": order_id, "service": order_update.service, "status": order_update.status}

@router.delete("/delete/{order_id}", response_model=dict)
def delete_order_route(order_id: str, username: str = Depends(verify_jwt), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_order(order_id)
    return {"message": f"Order {order_id} deleted successfully"}
