from flask import Flask, request, send_file, jsonify, make_response
from flask_cors import CORS
import io
from logger import logger

import cv
import lidata

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition", "X-Custom-Header"])  # Включаем поддержку CORS для всех маршрутов

@app.route('/api/url', methods=['POST'])
def handle_url():
    logger.info('Received request to handle URL')
    
    data = request.get_json()
    
    # Проверяем, есть ли URL в полученных данных
    if not data or 'url' not in data:
        return jsonify({"error": "URL is missing"}), 400
    
    url = data['url']
    
    try:
        logger.info('Receiving data for: %s',url)
        profile_data = lidata.get_profile_data(url)
    except Exception as e:
        logger.error('Error occurred while receiving data for: %s %s', url, e)
    
    try:
        logger.info('Creating profile document for: %s %s', url, e)
        file_stream, filename = cv.create_profile_document(profile_data)
    except Exception as e:
        logger.error('Error occurred while creating profile document: %s %s', url, e)
   
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
#   10. add calculation of dowload count


