from flask import jsonify

"""
Обработчик роута получения Short
"""
def prepare_video(data):
    return jsonify({"status": "ok", "result": "<insert url>"}), 200