from fastapi import HTTPException, Security, Depends, APIRouter
from sqlalchemy.orm import Session
from models import User, Order
from pydantic_models import UserCreate, UserResponse, OrderResponse
from fastapi.security import HTTPBearer
from database import get_db
import bcrypt
import jwt
import datetime
from mongodb import get_orders_by_user 

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
security = HTTPBearer()

# Добавляем объявление маршрутизатора
auth_router = APIRouter()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_superuser(db: Session):
    if not db.query(User).filter(User.username == "admin").first():
        hashed_password = hash_password("secret")
        admin_user = User(username="admin", password=hashed_password)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Superuser created!")

def create_jwt(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@auth_router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_jwt(db_user.username)

    # Получаем заказы пользователя из MongoDB
    order_list = get_orders_by_user(db_user.id)

    return {
        "user_id": db_user.id,
        "username": db_user.username,
        "token": token,
        "orders": order_list
    }

def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Создание JWT токена
    token = create_jwt(new_user.username)
    return UserResponse(username=new_user.username, token=token)

def verify_jwt(token: str = Security(security), db: Session = Depends(get_db)):
    """Проверка и валидация JWT токена"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.username == payload["sub"]).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
        return user.username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")