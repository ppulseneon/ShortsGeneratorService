import random
import re
import string
import textwrap

import numpy as np
from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from tools.text import insert_spaces_before_uppercase

# Определяем кастомные позиции текста
center = ('center', 'center')
top = ('center', 200)
bottom = ('center', 1920 - 500)

def random_movement(clip, t):
    movement_range = 20
    x_offset = random.uniform(-movement_range, movement_range)
    y_offset = random.uniform(-movement_range, movement_range)

    return (clip.w / 2 + x_offset, clip.h / 2 + y_offset)

def smooth_random_movement(clip, t):
    movement_range = 20  # pixels
    x_offset = movement_range * np.sin(t * 2 * np.pi / 5)
    y_offset = movement_range * np.cos(t * 2 * np.pi / 5)
    return (clip.w / 2 + x_offset, clip.h / 2 + y_offset)

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

def prepare_headline(headline):
    headline = textwrap.fill(headline, width=25)
    return headline

def prepare_subtitles(subtitles):
    for subtitle in subtitles:
        subtitle['text'] = insert_spaces_before_uppercase(subtitle['text'])

        subtitle['text'] = textwrap.fill(subtitle['text'], width=25)

        for p in string.punctuation:
            subtitle['text'] = subtitle['text'].replace(p, '')

        subtitle['text'] = subtitle['text'].upper()

    return subtitles

def animate_subtitles(clips, position):
    animated_clips = []
    for clip in clips:
        # animated_clip = clip.set_position(lambda t: random_movement(clip, t))
        # Alternatively, use smooth_random_movement for smoother motion
        animated_clip = clip.set_position(lambda t: smooth_random_movement(clip, t))
        animated_clips.append(animated_clip)

    return animated_clips

def generate_headline(clip, headline, duration, color):
    headline = prepare_headline(headline)
    text_clip = TextClip(headline, font='Roboto-Bold', fontsize=72, color=color)
    text_clip = text_clip.set_duration(duration)

    clip = CompositeVideoClip([clip, text_clip.set_position(get_position(0))])

    return clip

def generate_subtitles(subtitles, position: int, font_name: str, color: str, bg_color: (int, int, int), style: int) -> list[CompositeVideoClip]:
    subtitles = prepare_subtitles(subtitles)

    result = []

    if style < 0 or style > 2:
        raise ValueError(f"Invalid subtitle type value: {position}")

    match style:
        case 0:
            result = generate_clear_subtitles(subtitles, position, font_name, color, bg_color)
        case 1:
            result = generate_subtitles_with_outline(subtitles, position, font_name, color, bg_color)
        case 2:
            result = generate_subtitles_with_background(subtitles, position, font_name, color, bg_color)

    return result

def generate_clear_subtitles(subtitles, position: int, font_name: str, color: str, bg_color: (int, int, int)):
    text_clips = []

    # Проходимся по всем субтитрам
    for subtitle in subtitles:
        start_time, end_time = subtitle["timestamp"]
        text_clip = TextClip(subtitle['text'], font='Roboto-Bold', fontsize=64, color=color)
        text_clip = text_clip.set_duration(end_time - start_time)
        text_clip = text_clip.set_start(start_time)

        text_clip = text_clip.set_position(get_position(position))

        text_clips.append(text_clip)

    return text_clips

def generate_subtitles_with_outline(subtitles, position: int, font_name: str, color: str, bg_color: (int, int, int)):
    text_clips = []

    # Проходимся по всем субтитрам
    for subtitle in subtitles:
        start_time, end_time = subtitle["timestamp"]
        text = subtitle['text']
        color = 'white'
        outline_color = 'black'
        fontsize = 64
        outline_fontsize = fontsize + 1

        # Create the text clip with the outline
        text_clip_outline = TextClip(text, font='Roboto-Bold', fontsize=outline_fontsize, color=outline_color)
        text_clip_outline = text_clip_outline.set_duration(end_time - start_time)
        text_clip_outline = text_clip_outline.set_start(start_time)
        text_clip_outline = text_clip_outline.set_position(get_position(position))

        # Create the main text clip
        text_clip = TextClip(text, font='Roboto-Bold', fontsize=fontsize, color=color)
        text_clip = text_clip.set_duration(end_time - start_time)
        text_clip = text_clip.set_start(start_time)
        text_clip = text_clip.set_position(get_position(position))

        # Combine the outline and the main text clip
        combined_clip = CompositeVideoClip([text_clip_outline, text_clip]).set_position(get_position(position))

        text_clips.append(combined_clip)

    return text_clips

def generate_subtitles_with_background(subtitles, position: int, font_name: str, color: str, bg_color: (int, int, int)):
    text_clips = []

    # Проходимся по всем субтитрам
    for subtitle in subtitles:
        start_time, end_time = subtitle["timestamp"]
        text_clip = TextClip(subtitle['text'], font='Roboto-Bold', fontsize=64, color=color)
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

