from database import engine, SessionLocal
from models import Base, User, Order
from sqlalchemy.orm import Session
from auth import hash_password  # Для хеширования паролей
from mongodb import create_order
from pydantic_models import OrderCreate

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Подключение к базе данных
db = SessionLocal()

# Добавление тестовых данных
def create_test_data(db: Session):
    # Добавляем суперпользователя
    if not db.query(User).filter(User.username == "admin").first():
        hashed_password = hash_password("secret")
        admin_user = User(username="admin", password=hashed_password)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

create_test_data(db)

# Получаем ID суперпользователя
admin_user = db.query(User).filter(User.username == "admin").first()
if admin_user:
    # Проверяем, есть ли уже заказы в MongoDB
    from mongodb import get_orders_by_user
    existing_orders = get_orders_by_user(admin_user.id)

    if not existing_orders:
        # Добавляем тестовые заказы в MongoDB
        create_order(OrderCreate(user_id=admin_user.id, service="Cleaning", status="completed"))
        create_order(OrderCreate(user_id=admin_user.id, service="Plumbing", status="pending"))
        create_order(OrderCreate(user_id=admin_user.id, service="Electrician", status="in_progress"))

db.close()
