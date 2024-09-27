from moviepy.editor import *

class PrepareVideo:

    """
    Класс, предназначенный для создания коротких видео и превью для них
    """

    def __init__(self, video_path: str, short_timestamps: (float, float), primary_video_path: str = None, format_type: int = 0):

        # Формируем продолжительность короткого видео
        self.duration = short_timestamps[1] - short_timestamps[0]

        # Создаем новый пустой клип
        self.clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=self.duration)

    def set_subtitles(self, subtitles, position: int, color: int, bg_color: int, style: int):
        # todo: Реализовать логику добавления эмодзи в субтитры
        pass

    def set_background_music(self, music_path: str, volume: float = 1, offset: int = 0, finish: int = 0):
        pass

    def set_face_tracking(self):
        # todo: Подумать над реализацией этой идеи
        pass

    def render(self) -> str:
        pass

    def create_preview(self, short_name: str) -> str:
        pass