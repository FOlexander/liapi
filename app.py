from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io

import cv
import lidata

app = Flask(__name__)
CORS(app)  # Включаем поддержку CORS для всех маршрутов

@app.route('/api/url', methods=['POST'])
def handle_url():
    data = request.get_json()
    
    # Проверяем, есть ли URL в полученных данных
    if not data or 'url' not in data:
        return jsonify({"error": "URL is missing"}), 400
    
    url = data['url']
    profile_data = lidata.get_profile_data(url)
    file_stream, filename = cv.create_profile_document(profile_data)

    # Отправляем файл как ответ
    return send_file(
        file_stream,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name=filename
    )

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
