"""
pytest
"""

from check_chat_media import pic_expected, parse_chat_doc_medias, chat_doc_errors


def test_pic_expected_2():
    assert pic_expected('%pic:"foo.jpg" junk %pic:"bar.gif"') == ['foo.jpg', 'bar.gif']


def test_pic_expected_none():
    assert pic_expected('nothing') == []


relative_chat_path = 'a/b/c/file.cha'

media_root_dir = '/media'

media_dict = {
    '/media/a/b/c/x.mp3': '/media/a/b/c/X.mp3',
    '/media/a/b/c/y.mp4': '/media/a/b/c/y.mp4',
    '/media/a/b/c/j1.jpg': '/media/a/b/c/j1.jpg',
    '/media/a/b/c/j2.jpg': '/media/a/b/c/j2.jpg',
}

many_text = """
@Media:\ty, video
%pic:"j1.jpg" junk %pic:"j2.jpg"
"""

missing_video_text = """
@Media:\tx, video
%pic:"j1.jpg" junk %pic:"j2.jpg"
"""

wrong_case_text = """
@Media:\tx, audio
"""


def test_parse_chat_doc_medias():
    assert parse_chat_doc_medias(many_text) == [
        ('pic', 'j1.jpg'),
        ('pic', 'j2.jpg'),
        ('video', 'y'),
    ]


def test_chat_doc_errors_good():
    assert chat_doc_errors(relative_chat_path, many_text, media_root_dir, media_dict) == []


def test_chat_doc_errors_missing_video():
    assert chat_doc_errors(relative_chat_path, missing_video_text, media_root_dir, media_dict) == [
        ('missing', 'video', '/media/a/b/c/x.mp4')
    ]


def test_chat_doc_wrong_case():
    assert chat_doc_errors(relative_chat_path, wrong_case_text, media_root_dir, media_dict) == [
        ('incorrectly-cased /media/a/b/c/X.mp3', 'audio', '/media/a/b/c/x.mp3')
    ]
