import requests
from PIL.Image import Image
from flask import jsonify

from services.prepare_video_extensions.generation_preview import generate_preview
from tools.validation import validate_required_fields

required_fields = {
    'screenshot': str,
    'title': str
}

"""
Обработчик route получения превью
"""
def prepare_video(data):

    # Валидируем обязательные поля
    is_valid, error_message = validate_required_fields(data, required_fields)

    # Выбрасываем исключение, если какого-то из обязательных полей нет
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    screen = data['screenshot']
    title = data['title']
    position = data.get('position')

    image = Image.open(requests.get(screen, stream=True).raw)

    result = generate_preview(image, title, position)

    return jsonify({"status": "ok", "result": result}), 200