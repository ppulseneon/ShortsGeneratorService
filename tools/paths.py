import os
import uuid

from settings.settings import TEMP_FILES_FOLDER, STATIC_FILES_FOLDER

"""
Возвращает случайный путь для создания .mp4 файла
"""
def get_random_mp4_path():
    current_dir = os.getcwd()
    video_path = f"{current_dir}/{TEMP_FILES_FOLDER}/{uuid.uuid4()}.mp4"
    return video_path

def get_random_path(file_format: str):
    current_dir = os.getcwd()
    video_path = f"{current_dir}/{TEMP_FILES_FOLDER}/{uuid.uuid4()}.{file_format}"
    return video_path

def get_static_file(folder: str, filename: str):
    current_dir = os.getcwd()
    filepath = f"{current_dir}/{STATIC_FILES_FOLDER}/{folder}/{filename}"

    if not os.path.exists(filepath):
        print(filepath)
        raise Exception(f"Requested file is not stored in API storage")

    return filepath