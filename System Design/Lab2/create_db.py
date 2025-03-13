from database import engine, SessionLocal
from models import Base, User, Order
from sqlalchemy.orm import Session
from auth import hash_password  # Для хеширования паролей

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Добавление тестовых данных
def create_test_data(db: Session):
    # Добавляем суперпользователя
    if not db.query(User).filter(User.username == "admin").first():
        hashed_password = hash_password("secret")
        admin_user = User(username="admin", password=hashed_password)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

    # Добавляем тестовые заказы для пользователя
    user = db.query(User).filter(User.username == "admin").first()
    if user:
        if not db.query(Order).filter(Order.user_id == user.id).first():
            order1 = Order(user_id=user.id, service="Cleaning", status="completed")
            order2 = Order(user_id=user.id, service="Plumbing", status="pending")
            db.add(order1)
            db.add(order2)
            db.commit()

# Подключение к базе данных
db = SessionLocal()
create_test_data(db)
db.close()
