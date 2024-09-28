import re

import requests
import json

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
                "content": f"I have json. In each element of the text array, define a common emotions and return for one element one emotion in the 'emotions' field. Return only json. Emotions list: anger, disgust, ethusiasm, fear, guilt, joy, neutral, sadness, shame, surprise. Json: {subtitles}"
            }
        ]
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, json=data, headers=headers)

    # Check the response status code and content
    # print("Status code: ", response.status_code)
    # print("Response content: ", response.json())

    response_json = response.json()['response']

    print(response_json)

    emoji_subtitles = extract_content_between_brackets(response_json)

    print(emoji_subtitles)

    # Удаление символов новой строки
    emoji_subtitles = str.replace("\n", "")

    return emoji_subtitles + ']'

