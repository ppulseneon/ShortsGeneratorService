from flask import jsonify

from services.prepare_video import PrepareVideo
from tools.downloader import download_media
from tools.paths import get_random_mp4_path, get_random_path, get_static_file
from tools.validation import validate_required_fields

required_fields = {
    'original_id': int,
    'video': str,
    'short_timestamps_start': float,
    'short_timestamps_end': float,
    'music_file_type': int,
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

        original_id = int(data['original_id'])

        video = download_media(data['video'], video_path)
        format_type = int(data['format_type'])
        short_timestamp_start = data.get('short_timestamps_start')
        short_timestamp_end = data.get('short_timestamps_end')

        primary_video_path = data.get('primary_video')

        subtitles = int(data['subtitles'])

        music_file_type = int(data['music_file_type'])
        music = data.get('music')
        music_volume = data.get('music_volume')
        music_offset = data.get('music_offset')
        music_finish = data.get('music_finish')


        short_timestamp = (short_timestamp_start, short_timestamp_end)

        prepare = PrepareVideo(video, short_timestamps=short_timestamp, primary_video_path=primary_video_path, format_type=format_type, original_id=original_id)

        # Проверка наложения фоновой музыки
        if music_file_type != -1:

            # Проверка есть ли ссылка на песню/файл
            if not music:
                raise Exception(f"Music is required when music_file_type is not -1")

            # Инициализация пустого пути
            music_path = ''

            # По файлу
            if music_file_type == 1:
                music_path = get_static_file(music)

            # По ссылке
            if music_file_type == 1:
                music_path = get_random_path('mp3')
                download_media(music, music_path)

            # валидация полей
            if music_volume or music_finish or music_offset:
                raise Exception(f"Not all fields of music have been transferred")

            prepare.set_background_music(music_path, music_volume, music_offset, music_finish)

        result = prepare.render()

        if not result:
            return jsonify({"status": "error", "message": 'idk why throw error'}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "ok", "result": result}), 200