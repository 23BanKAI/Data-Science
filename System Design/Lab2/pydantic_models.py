from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class OrderResponse(BaseModel):
    order_id: str
    service: str
    status: str

class UserResponse(BaseModel):
    username: str
    token: str
    orders: List[OrderResponse] = []

    class Config:
        from_attributes = True
        
class OrderCreate(BaseModel):
    user_id: int
    service: str
    status: str = "pending"
