import os
import uuid

from settings.settings import TEMP_FILES_FOLDER

"""
Возвращает случайный путь для создания .mp4 файла
"""
def get_random_mp4_path():
    current_dir = os.getcwd()
    video_path = f"{current_dir}\\{TEMP_FILES_FOLDER}\\{uuid.uuid4()}.mp4"
    return video_path