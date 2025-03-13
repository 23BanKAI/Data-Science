#!/bin/bash

# Ожидание подключения к базе данных
until PGPASSWORD=password psql -h db -U postgres -d mydatabase -c '\q'; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# Выполнение скрипта создания базы данных и наполнения тестовыми данными
python /app/create_db.py

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000
