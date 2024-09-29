import requests

from settings.settings import FILE_SERVER_PRIVATE_KEY, FILE_SERVER_AUTH_TOKEN


class FileServerClient:
    def __init__(self):
        self.base_url = 'http://fileserver.enotgpt.ru'
        self.private_key = FILE_SERVER_PRIVATE_KEY
        self.token = FILE_SERVER_AUTH_TOKEN

    def binding_short(self, video_url, original_id):
        url = f'{self.base_url}/bindRecommendationToVideo'

        params = {
            "video_url": video_url,
            "original_id": original_id,
            "private_key": self.private_key,
        }

        response = requests.get(url, params=params)
        print(response.json())

        if response.status_code == 200:
            return True
        else:
            return False

    def upload_short(self, video_path) -> str | None:
        while True:
            url = f'{self.base_url}/video/upload_recommendation'

            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }

            files = {
                'file': ('result.mp4', open(video_path, 'rb'), 'video/mp4')
            }

            response = requests.post(url, headers=headers, files=files)

            print(response.json())

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:

                # На файловом сервере разорвало соединение с базой данных
                continue
            else:
                return None