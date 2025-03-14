FROM python:3.9

# Установка зависимостей для работы с PostgreSQL и MongoDB
RUN apt-get update && \
    apt-get install -y postgresql-client

# Установка зависимостей Python
WORKDIR /app
COPY . /app
COPY entrypoint.sh /app/entrypoint.sh
RUN pip install -r requirements.txt