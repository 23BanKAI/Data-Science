import jwt
import datetime
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer
from models import User, users_db
import hashlib

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
security = HTTPBearer()

MASTER_USERNAME = "admin"
MASTER_PASSWORD = "secret"

async def create_superuser():
    """Создание суперпользователя при старте приложения."""
    
    if MASTER_USERNAME not in users_db:
        hashed_password = hashlib.sha256(MASTER_PASSWORD.encode()).hexdigest()
        
        users_db[MASTER_USERNAME] = {
            "username": MASTER_USERNAME,
            "password": hashed_password
        }
        print("Суперпользователь создан!")
    else:
        print("Суперпользователь уже существует!")

def create_jwt(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str = Security(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")
