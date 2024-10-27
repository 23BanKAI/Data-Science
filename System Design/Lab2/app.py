from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
jwt = JWTManager(app)

# Временное хранилище данных
users = {}
services = {}

# Мастер-пользователь
master_user = {
    'username': 'admin',
    'password': generate_password_hash('secret')  # Хешируем пароль
}

users[master_user['username']] = master_user

# Роут для корня
@app.route('/')
def home():
    return "Welcome to the Service API. Use /login, /users, or /services endpoints."

# Роут для аутентификации
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = users.get(username)

    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401

# Роут для управления пользователями
@app.route('/users', methods=['GET', 'POST'])
@jwt_required()
def manage_users():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        if username in users:
            return jsonify({'msg': 'User already exists'}), 400

        users[username] = {
            'username': username,
            'password': generate_password_hash(password)
        }
        return jsonify({'msg': 'User created'}), 201

    return jsonify(users), 200

# Пример бизнес-сервиса: управление услугами
@app.route('/services', methods=['GET', 'POST'])
@jwt_required()
def manage_services():
    if request.method == 'POST':
        service_name = request.json.get('service_name')

        if service_name in services:
            return jsonify({'msg': 'Service already exists'}), 400

        services[service_name] = {
            'name': service_name
        }
        return jsonify({'msg': 'Service created'}), 201

    return jsonify(services), 200

if __name__ == '__main__':
    app.run(debug=True)
