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
    'subtitles': int
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

        subtitles_json = data.get('subtitles_json')
        subtitles_position = data.get('subtitles_position')
        subtitles_font = data.get('subtitles_font')
        subtitles_color = data.get('subtitles_color')

        subtitles_bg_color_r = data.get('subtitles_bg_color_r')
        subtitles_bg_color_g = data.get('subtitles_bg_color_g')
        subtitles_bg_color_b = data.get('subtitles_bg_color_b')

        headline = data.get('headline')
        headline_color = data.get('headline_color')

        short_timestamp = (short_timestamp_start, short_timestamp_end)

        prepare = PrepareVideo(video, short_timestamps=short_timestamp, primary_video_path=primary_video_path, format_type=format_type, original_id=original_id)

        # Проверка наложения субтитров
        if subtitles != -1:

            # валидация полей
            if not subtitles_font or not subtitles_color or not subtitles_json:
                raise Exception(f"Not all fields of subtitles have been transferred")

            subtitles_primary_color = (subtitles_bg_color_r, subtitles_bg_color_g, subtitles_bg_color_b)

            prepare.set_subtitles(subtitles_json, short_timestamp_start, subtitles_position, subtitles_font, subtitles_color, subtitles_primary_color, subtitles)

        if headline and subtitles_position != 0:
            if not headline_color:
                raise Exception(f"Headline color is required")

            prepare.set_headline(headline, headline_color)

        # Проверка наложения фоновой музыки
        if music_file_type != -1:

            # Проверка есть ли ссылка на песню/файл
            if not music:
                raise Exception(f"Music is required when music_file_type is not -1")

            # Инициализация пустого пути
            music_path = ''

            # По файлу
            if music_file_type == 1:
                music_path = get_static_file('music', music)

            # По ссылке
            if music_file_type == 1:
                music_path = get_random_path('mp3')
                download_media(music, music_path)

            # валидация полей
            if not music_volume or not music_finish or not music_offset:
                raise Exception(f"Not all fields of music have been transferred")

            prepare.set_background_music(music_path, music_volume, music_offset, music_finish)

        result = prepare.render()

        if not result:
            return jsonify({"status": "error", "message": 'idk why throw error'}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "ok", "result": result}), 200