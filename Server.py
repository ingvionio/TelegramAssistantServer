from flask import Flask, request, jsonify
from flask_cors import CORS  # Добавляем поддержку CORS

app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов

# Пример базы данных маршрутов
user_routes = {}
user_final_routes = {}

@app.route('/api/save-routes', methods=['POST'])
def save_routes():
    data = request.json
    user_id = data.get('user_id')
    routes = data.get('routes')

    if not user_id or not routes:
        return jsonify({"error": "Необходимы user_id и routes"}), 400

    user_routes[user_id] = routes
    print(f"Маршруты для пользователя {user_id} сохранены")
    return jsonify({"success": True})

@app.route('/api/save-final-routes', methods=['POST'])
def save_final_routes():
    data = request.json
    user_id = data.get('user_id')
    routes = data.get('route')

    if not user_id or not routes:
        return jsonify({"error": "Необходимы user_id и routes"}), 400

    user_final_routes[user_id] = routes
    print(f"Итоговый маршрут пользователя {user_id} сохранены")
    return jsonify({"success": True})

@app.route('/api/final-routes', methods=['GET'])
def get_final_routes():
    user_id = request.args.get('user_id')

    if not user_id:
        print("Ошибка: Отсутствует user_id")
        return jsonify({"error": "Отсутствует user_id"}), 400

    if user_id not in user_routes:
        print(f"Ошибка: Маршруты для пользователя {user_id} не найдены")
        return jsonify({"error": "Маршруты не найдены"}), 404

    print(f"Отправляем маршруты для пользователя {user_id}")
    response = jsonify(user_final_routes[user_id])
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route('/api/routes', methods=['GET'])
def get_routes():
    user_id = request.args.get('user_id')

    if not user_id:
        print("Ошибка: Отсутствует user_id")
        return jsonify({"error": "Отсутствует user_id"}), 400

    if user_id not in user_routes:
        print(f"Ошибка: Маршруты для пользователя {user_id} не найдены")
        return jsonify({"error": "Маршруты не найдены"}), 404

    print(f"Отправляем маршруты для пользователя {user_id}")
    response = jsonify(user_routes[user_id])
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Слушаем все интерфейсы