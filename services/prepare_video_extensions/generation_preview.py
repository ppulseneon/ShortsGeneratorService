import textwrap

from PIL.Image import Image
from moviepy.video.VideoClip import ImageClip, TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

center = ('center', 960)
top = ('center', 'center')
bottom = ('center', 1920 - 500)

def generate_preview(screen: Image, title: str, position: int):
    preview = ImageClip(screen).resize(1080, 1920)

    title = textwrap.fill(title, width=25)

    title_clip = TextClip(title, font='Roboto-Bold', fontsize=72, color='white')

    title.set_position('center')

    image_width, image_height = title_clip.size
    padding_width = 20
    padding_height = 20

    color_clip = ColorClip(size=(image_width + padding_width,
                                 image_height + padding_height),
                           color=(0, 0, 0))

    title_composite = CompositeVideoClip([color_clip, title_clip])
    preview_composite = CompositeVideoClip([title_composite, preview])

    return preview_composite