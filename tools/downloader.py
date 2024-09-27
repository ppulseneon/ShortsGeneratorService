import os

import requests

"""
    Метод для загрузки видео по ссылке
"""
def download_video(url, filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)

    print(f"Video downloaded and saved as {filename}")
    return filename
