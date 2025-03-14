import redis
import json
from typing import List
from pydantic_models import OrderResponse
from typing import List, Optional

# Подключение к Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Ключ для хранения заказов в кэше (по пользователю)
def get_cache_key(user_id: int) -> str:
    return f"user_orders:{user_id}"

# Функция для сохранения заказов в Redis
def cache_orders(user_id: int, orders: List[OrderResponse], ttl: int = 600):
    orders_data = [order.dict() for order in orders]
    redis_client.setex(get_cache_key(user_id), ttl, json.dumps(orders_data))

# Функция для получения заказов из Redis
def get_cached_orders(user_id: int) -> Optional[List[OrderResponse]]:
    cached_data = redis_client.get(get_cache_key(user_id))
    if cached_data:
        return [OrderResponse(**order) for order in json.loads(cached_data)]
    return None

# Удаление кэша при обновлении данных
def invalidate_cache(user_id: int):
    redis_client.delete(get_cache_key(user_id))