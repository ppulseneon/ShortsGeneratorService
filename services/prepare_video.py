import json
import random

from moviepy.editor import *

from services.fileserver_client import FileServerClient
from services.lama_client import updated_subtitres
from services.prepare_video_extensions.formatting_video import FormattingVideo
from services.prepare_video_extensions.generation_subtitles import generate_subtitles, offset_subtitles_for_shorts, \
    animate_subtitles, generate_headline, cut_subtitles_by_timestamp, generate_emotions
from tools.paths import get_random_mp4_path


class PrepareVideo:

    """
    Класс, предназначенный для создания коротких видео и превью для них
    """
    def __init__(self, video_path: str, short_timestamps: (float, float), original_id: int, primary_video_path: str = None, format_type: int = 0):

        # Формируем продолжительность короткого видео
        self.duration = short_timestamps[1] - short_timestamps[0]

        # Создаем новый пустой клип
        self.clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=self.duration)

        # Устанавливаем главный клип из видео
        self.main_clip = VideoFileClip(video_path).subclip(short_timestamps[0], short_timestamps[1])

        # Устанавливаем интересное видео
        if primary_video_path is not None:
            # self.primary_clip = VideoFileClip(primary_video_path).subclip(0, self.clip.duration)
            self.primary_clip = VideoFileClip(primary_video_path)

            # Определяем рамки дополнительного клипа
            if self.primary_clip.duration < self.duration:

                # Указываем длину и оставляем как есть (доп. Видео будет короче, чем основное?)
                primary_timestamp = self.primary_clip.duration

                # todo: по кругу его пустить

            else:
                # Получаем максимальную длину рандома
                primary_timestamp_border = self.primary_clip.duration - self.duration

                # Получаем рандомный край видео
                primary_timestamp_end = random.randint(int(self.duration), int(primary_timestamp_border))

                # Определяем начало и конец
                primary_timestamp = (primary_timestamp_end - self.duration, primary_timestamp_end)

                # Устанавливаем временные рамки доп. Видео
                self.primary_clip = self.primary_clip.subclip(primary_timestamp[0], primary_timestamp[1])
                self.primary_clip = self.primary_clip.set_duration(self.clip.duration)
        else:
            self.primary_clip = None

        formatter = FormattingVideo(format_type=format_type, blank_clip=self.clip, main_clip=self.main_clip, primary_clip=self.primary_clip)
        self.clip = formatter.set_video_format()

        self.original_id = original_id

    """
    Метод для добавления субтитров
    """
    def set_subtitles(self, subtitles, timestamp_start: float, timestamp_end: float, position: int, font_name: str, color: str, bg_color: (int, int, int), style: int, emotions):
        # todo: Реализовать логику добавления эмодзи в субтитры

        # Обрезаем субтитры
        subtitles = cut_subtitles_by_timestamp(json.loads(subtitles.replace("'", '"')), timestamp_start, timestamp_end)

        # Сдвиг субтитр
        subtitles = offset_subtitles_for_shorts(subtitles, timestamp_start)

        # Получаем субтитры с эмоциями эмоции
        subtitles = updated_subtitres(subtitles)

        # Все текстовые элементы
        subtitles_clips = generate_subtitles(subtitles, position, font_name, color, bg_color, style)

        # Анимированные клипы
        # subtitles_clips = animate_subtitles(subtitles_clips, position)

        if emotions:
            # Все клипы эмоций
            emotions_clips = generate_emotions(subtitles, position)

            # Объедините видео и текстовые клипы
            self.clip = CompositeVideoClip([self.clip] + subtitles_clips + emotions_clips)

        else:
            # Объедините видео и текстовые клипы
            self.clip = CompositeVideoClip([self.clip] + subtitles_clips)



    """
        Метод для добавления текста сверху
    """
    def set_headline(self, headline, color):
        result = generate_headline(self.clip, headline, self.clip.duration, color)

        self.clip = result

    """
    Метод для добавления фоновой музыки
    """
    def set_background_music(self, music_path: str, volume: float = 1, offset: int = 0, finish: int = 0):

        # Указываем аудиодорожку
        audio_clip = AudioFileClip(music_path)

        # Подрезаем начало и конец накладываемого трека
        audio_clip = audio_clip.subclip(offset, self.clip.duration - finish)

        # Проверка тречка
        if audio_clip.duration == 0:
            raise ValueError("Audio clip has zero duration")

        # Получаем текущую дорожку из видео
        clip_audio = self.clip.audio

        # Устанавливаем громкость
        audio_clip = audio_clip.volumex(volume)

        # Смешиваем обе дорожки в одну
        final_audio = CompositeAudioClip([clip_audio, audio_clip])

        # Устанавливаем аудиодорожку видео
        self.clip = self.clip.set_audio(final_audio)

    """
    Метод для добавления слежки за лицами
    """
    def set_face_tracking(self):
        # todo: Подумать над реализацией этой идеи
        pass

    """
    Метод для рендера видео
    """
    def render(self) -> str | None:
        path = get_random_mp4_path()
        return self.render_with_path(path)

    """
        Метод для рендера видео
    """
    def render_with_path(self, path: str) -> str | None:
        self.clip.write_videofile(path)

        fileserver = FileServerClient()

        print(f'Saved video: {path}')

        # Загружаем шортс на сервер
        upload_result = fileserver.upload_short(path)

        # Если не загрузило
        if not upload_result:
            return None

        # Биндим шортс
        bind_result = fileserver.binding_short(upload_result, self.original_id)

        # Проверяем результат
        # if not bind_result:
        #     return None

        # Удаляем временные файлы
        # os.remove(self.main_clip.path)
        # os.remove(path)

        print(f'Clip was rendered')
        return upload_result

    def create_preview(self, short_name: str) -> str:
        pass