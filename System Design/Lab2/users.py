from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic_models import UserCreate, UserResponse  # Импортируем Pydantic модели
from models import User  # Импортируем SQLAlchemy модель
from database import get_db
import bcrypt
import jwt
import datetime
from auth import verify_jwt

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def create_jwt(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=UserResponse)  # Используем UserResponse для ответа
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Хешируем пароль
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Создаем JWT токен
    token = create_jwt(new_user.username)
    
    return UserResponse(username=new_user.username, token=token)

@router.put("/update", response_model=UserResponse)
def update_user(user_update: UserCreate, db: Session = Depends(get_db), username: str = Depends(verify_jwt)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем пароль, если он передан
    if user_update.password:
        db_user.password = bcrypt.hashpw(user_update.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db.commit()
    db.refresh(db_user)
    
    return UserResponse(username=db_user.username, token=create_jwt(db_user.username))

@router.delete("/delete", response_model=dict)
def delete_user(db: Session = Depends(get_db), username: str = Depends(verify_jwt)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    
    return {"message": f"User {username} deleted successfully"}