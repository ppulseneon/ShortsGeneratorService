import re
import requests

def extract_content_between_brackets(text):
    start_marker = "```json"
    end_marker = "]\n```"

    json_start = text.find(start_marker) + len(start_marker)
    json_end = text.find(end_marker)

    json_string = text[json_start:json_end]

    return json_string


def updated_subtitres(subtitles):
    url = 'http://llm.enotgpt.ru/llama_ollama'

    data = {
        "data": [
            {
                "role": "user",
                "content": f"In each element of the text array, define a common emotions and return for one element one emotion in the 'emotion' field. Return only json. Emotions list: anger, disgust, enthusiasm, fear, guilt, joy, neutral, sadness, shame, surprise. Response format: [{{ 'timestamp': [value, value], 'text': 'text', 'emotion': 'emotion' }}].  Json: {subtitles}"
            }
        ]
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        response_json = response.json()['response']

        emoji_subtitles = extract_content_between_brackets(response_json)

        # Удаление символов новой строки
        emoji_subtitles = emoji_subtitles.replace("\n", "")
        emoji_subtitles = emoji_subtitles.replace("`", "")

        result = emoji_subtitles + ']'

        emotions = re.findall(r'"emotion":\s*"([^"]+)"', result)

        print('lama result ' + result)

        print(f'emotions: {len(emotions)} / subtitles: {len(subtitles)}')

        for i in range(len(subtitles)):
            subtitles[i]['emotion'] = emotions[i]

        return subtitles

    except Exception as e:
        for i in range(len(subtitles)):
            subtitles[i]['emotion'] = None

        return subtitles
