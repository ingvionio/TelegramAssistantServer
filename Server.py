from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Добавляем поддержку CORS

app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов
load_dotenv()  # Загружаем переменные из .env

BOT_TOKEN = os.getenv("BOT_TOKEN")

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

@app.route('/api/send-pdf', methods=['POST'])
def send_pdf():
    if 'document' not in request.files or 'chat_id' not in request.form:
        return jsonify({'error': 'Необходимо передать PDF и chat_id'}), 400

    file = request.files['document']
    chat_id = request.form['chat_id']

    if not BOT_TOKEN:
        return jsonify({'error': 'BOT_TOKEN не установлен на сервере'}), 500

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    files = {
        'document': (secure_filename(file.filename), file.stream, file.mimetype)
    }

    data = {
        'chat_id': chat_id,
        'caption': 'Ваш маршрут в PDF формате!'
    }

    response = requests.post(url, files=files, data=data)

    if response.ok:
        message_id = response.json()['result']['message_id']

        # Отправляем inline-кнопку
        keyboard = {
            'inline_keyboard': [[{
                'text': 'Добавить путешествие в календарь',
                'callback_data': 'add_event'
            }]]
        }

        edit_url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup"
        edit_data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': keyboard
        }

        requests.post(edit_url, json=edit_data)

        return jsonify({'success': True})
    else:
        print("Ошибка Telegram API:", response.text)
        return jsonify({'error': 'Не удалось отправить PDF'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Слушаем все интерфейсы