from flask import Flask, request, jsonify, redirect

from settings.static_files import fonts_list, format_types_list, primary_videos, music_list
from settings.swagger_settings import swagger_ui_blueprint, SWAGGER_URL

app = Flask(__name__)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

"""
Редирект с главной на Swagger 
"""
@app.route('/')
def hello_world():
    return redirect("/swagger", code=302)

"""
Получить Short из видео
"""
@app.route('/video', methods=['POST'])
def prepare_video():
    data = request.get_json()
    result = prepare_video(data)
    return result

"""
Получить доступные форматы видео
"""
@app.route('/video/format_type', methods=['GET'])
def get_format_type():
    return jsonify(format_types_list)

"""
Получить доступные шрифты для субтитров
"""
@app.route('/video/subtitles/fonts', methods=['GET'])
def get_fonts():
    return jsonify(fonts_list)

"""
Получить доступные завлекающие видео
"""
@app.route('/video/primary_videos', methods=['GET'])
def get_primary_videos():
    return jsonify(primary_videos)

"""
Получить доступную фоновую музыку
"""
@app.route('/video/music', methods=['GET'])
def get_music():
    return jsonify(music_list)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
