from pymongo import MongoClient, ASCENDING
from pydantic_models import OrderCreate, OrderResponse
from models import Order
from typing import List

MONGO_URL = "mongodb://mongo:27017/mydatabase"
client = MongoClient(MONGO_URL)
db = client.mydatabase
orders_collection = db.orders

# Создаем индексы для быстрого поиска
orders_collection.create_index([("user_id", ASCENDING)])

def create_order(order: OrderCreate):
    order_data = {
        "user_id": order.user_id,
        "service": order.service,
        "status": order.status
    }
    result = orders_collection.insert_one(order_data)
    return str(result.inserted_id)

def get_orders_by_user(user_id: int) -> List[OrderResponse]:
    orders = orders_collection.find({"user_id": user_id})
    return [OrderResponse(order_id=str(order["_id"]), service=order["service"], status=order["status"]) for order in orders]

def update_order(order_id: str, order: OrderCreate):
    orders_collection.update_one(
        {"_id": order_id},
        {"$set": {"service": order.service, "status": order.status}}
    )

def delete_order(order_id: str):
    orders_collection.delete_one({"_id": order_id})
