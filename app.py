from flask import Flask, request, send_file, jsonify, make_response
from flask_cors import CORS
import io

import cv
import lidata

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition", "X-Custom-Header"])  # Включаем поддержку CORS для всех маршрутов

@app.route('/api/url', methods=['POST'])
def handle_url():
    data = request.get_json()
    
    # Проверяем, есть ли URL в полученных данных
    if not data or 'url' not in data:
        return jsonify({"error": "URL is missing"}), 400
    
    url = data['url']
    profile_data = lidata.get_profile_data(url)
    file_stream, filename = cv.create_profile_document(profile_data)

    # Чтение содержимого файла как байты
    file_bytes = file_stream.read()

    # Создание ответа с байтовым содержимым файла
    response = make_response(file_bytes)
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['X-Custom-Header'] = 'YourCustomValue'
    
    return response

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#TODO
#   1. add logs
#   2. add error handling
#   3. add ips
#   4. add linkedind accounts
#   5. add response in case of error
#   6. add docs
#   7. add beauty html\css for popup
#   8. define details about personal account
#   9. check each fields in cv.py


