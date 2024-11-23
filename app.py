from flask import Flask, request, jsonify, make_response, g
from flask_cors import CORS
import io
import sqlite3
from logger import logger
import cv
import lidata

app = Flask(__name__)
CORS(app)

# Путь к базе данных
DATABASE = 'requests.db'

# Функция для подключения к базе данных SQLite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Создание таблицы для хранения информации о запросах
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                ip_address TEXT,
                browser TEXT,
                platform TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

# Закрытие подключения к базе данных после запроса
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/url', methods=['GET', 'POST', 'OPTIONS'])
def handle_url():
    # Чтение JSON-данных
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "URL is missing"}), 400
    
    url = data['url']
    
    # Получаем данные о клиенте
    ip_address = request.remote_addr
    browser = request.user_agent.browser
    platform = request.user_agent.platform

    try:
        # Логируем и получаем данные профиля
        logger.info('Receiving data for: %s', url)
        profile_data = lidata.get_profile_data(url)
    except Exception as e:
        logger.error('Error occurred while receiving data for: %s', url)
        logger.error(e)
        return jsonify({"error": "Error retrieving profile data"}), 500
    
    try:
        # Логируем и создаем документ профиля
        logger.info('Creating profile document for: %s', url)
        file_stream, filename = cv.create_profile_document(profile_data[0], profile_data[1])
    except Exception as e:
        logger.error('Error occurred while creating profile document: %s', url)
        logger.error(e)
        return jsonify({"error": "Error creating profile document"}), 500

    # Сохраняем данные в базе данных
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO requests (url, ip_address, browser, platform)
            VALUES (?, ?, ?, ?)
        ''', (url, ip_address, browser, platform))
        db.commit()
    except Exception as e:
        logger.error('Error occurred while saving to the database: %s', str(e))
        return jsonify({"error": "Error saving to database"}), 500
    
    # Формируем ответ с файлом
    response = make_response(file_stream.read())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

# Инициализируем базу данных при запуске приложения
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)


#TODO
#   
#   3. add ips
#   4. add linkedind accounts
#   6. add docs
#   8. define details about personal account
#   11. add limitation for download from one ip 5 per day
#   10. add calculation of dowload count / Done
#   2. add error handling / Done
#   9. check each fields in cv.py / Done
#   7. add beauty html\css for popup / Done
#   5. add response in case of error / Done
#   1. PROBLEM WITH CHOOSING IMG / Done





