import re
import textwrap

from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from tools.text import insert_spaces_before_uppercase

# Определяем кастомные позиции текста
center = ('center', 'center')
top = ('center', 200)
bottom = ('center', 1920 - 500)

def get_position(position):
    print(position)
    match position:
        case 0:
            return top
        case 1:
            return center
        case 2:
            return bottom

    raise ValueError(f"Invalid subtitle position: {position}")

def offset_subtitles_for_shorts(subtitles, offset):
    for subtitle in subtitles:
        subtitle['timestamp'][0] = subtitle['timestamp'][0] - offset
        subtitle['timestamp'][1] = subtitle['timestamp'][1] - offset

    return subtitles

def prepare_subtitles(subtitles):
    for subtitle in subtitles:
        subtitle['text'] = insert_spaces_before_uppercase(subtitle['text'])

        subtitle['text'] = textwrap.fill(subtitle['text'], width=25)

        subtitle['text'] = re.sub(r"(\w)([A-Z])", r"\1 \2", subtitle['text'])

        subtitle['text'] = subtitle['text'].upper()

    return subtitles

def generate_subtitles(subtitles, position: int, font_name: str, color: int, bg_color: int, style: int) -> list[CompositeVideoClip]:
    subtitles = prepare_subtitles(subtitles)

    result = []

    if style < 0 or style > 2:
        raise ValueError(f"Invalid subtitle type value: {position}")

    match style:
        case 0:
            result = generate_clear_subtitles(subtitles, position, font_name, color, bg_color)
        case 2:
            result = generate_subtitles_with_background(subtitles, position, font_name, color, bg_color)

    return result

def generate_clear_subtitles(subtitles, position: int, font_name: str, color: int, bg_color: int):
    text_clips = []

    # Проходимся по всем субтитрам
    for subtitle in subtitles:
        start_time, end_time = subtitle["timestamp"]
        text_clip = TextClip(subtitle['text'], font=font_name, fontsize=32, color=color)
        text_clip = text_clip.set_duration(end_time - start_time)
        text_clip = text_clip.set_start(start_time)

        text_clip = text_clip.set_position(get_position(position))

        text_clips.append(text_clip)

    return text_clips

def generate_subtitles_with_background(subtitles, position: int, font_name: str, color: str, bg_color: (int, int, int)):
    text_clips = []

    # Проходимся по всем субтитрам
    for subtitle in subtitles:
        start_time, end_time = subtitle["timestamp"]
        text_clip = TextClip(subtitle['text'], font='Roboto', fontsize=52, color=color)
        text_clip = text_clip.set_duration(end_time - start_time)
        text_clip = text_clip.set_start(start_time)

        image_width, image_height = text_clip.size

        padding_width = 20
        padding_height = 20
        color_clip = ColorClip(size=(image_width + padding_width,
                                     image_height + padding_height),
                               color=(0, 0, 0))

        text_clip = text_clip.set_position('center')

        color_clip = color_clip.set_duration(end_time - start_time)
        color_clip = color_clip.set_start(start_time)

        text_clip = CompositeVideoClip([color_clip, text_clip])
        text_clip = text_clip.set_position(get_position(position))

        text_clips.append(text_clip)

    return text_clips

