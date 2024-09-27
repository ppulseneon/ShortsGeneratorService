from flask import jsonify

from services.prepare_video import PrepareVideo
from tools.downloader import download_video
from tools.paths import get_random_mp4_path
from tools.validation import validate_required_fields

required_fields = {
    'original_id': int,
    'video': str,
    'short_timestamps_start': float,
    'short_timestamps_end': float,
}

"""
Обработчик route получения short
"""
def prepare_video(data):

    # Валидируем обязательные поля
    is_valid, error_message = validate_required_fields(data, required_fields)

    # Выбрасываем исключение, если какого-то из обязательных полей нет
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400

    # Сохраняем во временном хранилище ролик
    try:
        video_path = get_random_mp4_path()

        video = download_video(data['video'], video_path)
        primary_video_path = data.get('primary_video')
        short_timestamp_start = data.get('short_timestamps_start')
        short_timestamp_end = data.get('short_timestamps_end')
        original_id = int(data['original_id'])
        format_type = int(data['format_type'])
        subtitles = int(data['subtitles'])

        short_timestamp = (short_timestamp_start, short_timestamp_end)

        prepare = PrepareVideo(video, short_timestamps=short_timestamp, primary_video_path=primary_video_path, format_type=format_type, original_id=original_id)

        result = prepare.render()

        if not result:
            return jsonify({"status": "error", "message": 'idk why throw error'}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "ok", "result": result}), 200