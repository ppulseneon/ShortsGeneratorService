from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io import VideoFileClip

from tools.blur import blur_frame


class FormattingVideo:
    """
        Класс, для приведения видео в шаблонный формат
    """
    def __init__(self, format_type: int, blank_clip: VideoFileClip, main_clip: VideoFileClip, primary_clip):
        self.height = 1920
        self.width = 1080
        self.format_type = format_type
        self.blank_clip = blank_clip
        self.main_clip = main_clip
        self.primary_clip = primary_clip

    """
        Метод для установки формата короткого ролика
    """
    def set_video_format(self):
        if self.format_type > 6 or self.format_type < 0:
            raise ValueError(f"Invalid format_type: {self.format_type}. It must be between 0 and 6")

        match self.format_type:
            case 0:
                self._set_video_format_center_black_background()
            case 1:
                self._set_video_format_bigger_center_black_background()
            case 2:
                self._set_video_format_blurred_black_background()
            case 3:
                self._set_video_format_bigger_blurred_black_background()
            case 4:
                self._set_video_format_fullscreen()
            case 5:
                self._set_video_format_top_and_bottom_primary()
            case 6:
                self._set_video_format_primary_and_top_primary()

        return self.blank_clip

    """
        Метод, для преобразования видео по шаблону "Полноразмерное видео по центру, черный фон"
    """
    def _set_video_format_center_black_background(self):

        # Форматируем его под 9:16
        resized_height = int(self.width * (9/16))

        # Меняем размер клипа на 9:16 с шириной всего экрана
        resized_clip = self.main_clip.resize((self.width, resized_height))

        # Устанавливаем этот клип на полотне по центру
        self.blank_clip = CompositeVideoClip([self.blank_clip, resized_clip.set_position('center')])

    """
        Метод, для преобразования видео по шаблону "Увеличенное полноразмерное видео по центру, черный фон"
    """
    def _set_video_format_bigger_center_black_background(self):
        self.width = 1920

        # Форматируем его под 9:16
        resized_height = int(self.width * (9/16))

        # Меняем размер клипа на 9:16 с шириной всего экрана
        resized_clip = self.main_clip.resize((self.width, resized_height))

        # Устанавливаем этот клип на полотне по центру
        self.blank_clip = CompositeVideoClip([self.blank_clip, resized_clip.set_position('center')])

    """
        Метод, для преобразования видео по шаблону "Полноразмерное видео по центру, размытый фон"
    """
    def _set_video_format_blurred_black_background(self):
        # Форматируем его под 9:16
        resized_height = int(self.width * (9 / 16))

        # Ресайзед блюр
        resized_clip = self.main_clip.resize((1440, self.height))
        blurred_clip = resized_clip.fl_image(blur_frame)

        # Меняем размер клипа на 9:16 с шириной всего экрана
        resized_clip = self.main_clip.resize((self.width, resized_height))

        # Устанавливаем этот клип на полотне по центру
        self.blank_clip = CompositeVideoClip([self.blank_clip, resized_clip.set_position('center')])

    """
        Метод, для преобразования видео по шаблону "Увеличенное полноразмерное видео по центру, размытый фон"
    """
    def _set_video_format_bigger_blurred_black_background(self):
        self.width = 1920

        # Форматируем его под 9:16
        resized_height = int(self.width * (9 / 16))

        # Ресайзед блюр
        resized_clip = self.main_clip.resize((1440, self.height))
        blurred_clip = resized_clip.fl_image(blur_frame)

        # Меняем размер клипа на 9:16 с шириной всего экрана
        resized_clip = self.main_clip.resize((self.width, resized_height))

        # Устанавливаем этот клип на полотне по центру
        self.blank_clip = CompositeVideoClip([self.blank_clip, resized_clip.set_position('center')])

    """
        Метод, для преобразования видео по шаблону "Видео на весь экран"
    """
    def _set_video_format_fullscreen(self):
        width = 3408
        height9x16 = int(width * (9 / 16))

        resized_clip = self.main_clip.resize((width, height9x16))

        self.clip = CompositeVideoClip([self.blank_clip, resized_clip.set_position('center')])

    """
        Метод, для преобразования видео по шаблону "Сверху видео, снизу доп. видео"
    """
    def _set_video_format_top_and_bottom_primary(self):
        width = 1704
        height9x16 = int(width * (9 / 16))

        resized_clip = self.main_clip.resize((width, height9x16))
        resized_primary_clip = self.primary_clip.resize((width, height9x16))

        self.clip = CompositeVideoClip([self.blank_clip, resized_clip.set_position('top'), resized_primary_clip.set_position('bottom')])

    """
        Метод, для преобразования видео по шаблону "Сверху видео, снизу доп. видео"
    """
    def _set_video_format_primary_and_top_primary(self):
        width = 1704
        height9x16 = int(width * (9 / 16))

        resized_clip = self.main_clip.resize((width, height9x16))
        resized_primary_clip = self.primary_clip.resize((width, height9x16))

        self.clip = CompositeVideoClip([self.blank_clip, resized_clip.set_position('bottom'), resized_primary_clip.set_position('top')])