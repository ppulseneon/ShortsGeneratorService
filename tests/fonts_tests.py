from services.prepare_video import PrepareVideo

source = 'source.mp4'

subtitles = "[{ 'timestamp': [ 0, 2.06 ], 'text': 'быть талант корн, а у кого-то может' }, { 'timestamp': [ 2.06, 3.96 ], 'text': ' не получаться, например. У тебя все' }, { 'timestamp': [ 3.96, 5.3 ], 'text': ' получится. А если ты сейчас об этом,' }, { 'timestamp': [ 5.72, 7.96 ], 'text': ' верь в себя, ну правда. Ну нет,' }, { 'timestamp': [ 8.02, 9.82 ], 'text': 'мне интересно. Кто-то же становится' }]"

def test_font_fade():
    short_timestamp = (0, 9)
    prepare = PrepareVideo(source, short_timestamp, 0, None, 1)
    prepare.set_subtitles(subtitles, short_timestamp[0], 1, '', 'white', (0, 0, 0), 1)
    prepare.set_headline('Подписывайтесь на мой телеграм канал', 'white')
    prepare.render_with_path('result.mp4')

test_font_fade()