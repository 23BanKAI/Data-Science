from pydantic import BaseModel
from typing import List

users_db = {}

class User(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    token: str

class Order(BaseModel):
    order_id: int
    user: str
    service: str
    status: str = "pending"
