#!/usr/local/bin/python3

import sys
import os
import click
import subprocess
import re

media_re = re.compile(
    r"""
    ^@Media:\t
    ([^ ,]+)
    \ *,\ *
    (audio|video)
    (\ *,\ *(?:missing|unlinked))?
    """,
    re.X | re.MULTILINE
)


pic_re = re.compile(
    """%pic:
    "
    ([^\"]+)
    "
    """,
    re.X
)

@click.command()
@click.option('--chatdir', required=True, help='CHAT root dir')
@click.option('--host', required=True, help='Host name of media')
@click.option('--mediadir', required=True, help='Media root dir on host')
def main(chatdir, host, mediadir):
    """
    Print errors to stdout.
    """
    media_dict = get_media_dict(host, mediadir)

    num_errors = 0
    for doc_errors in all_media_errors(chatdir, mediadir, media_dict):
        for message, media_type, name in doc_errors:
            num_errors += 1
            print(f'{host}:{name}: {media_type} {message}')
    if num_errors != 0:
        sys.exit(1)


def get_media_dict(server, media_root_dir):
    """
    Return dict of lowercased absolute path to actual path in media_root_dir.
    """
    result = subprocess.run(
        ['ssh',
         server,
         'find',
         media_root_dir,
        ],
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    result.check_returncode()
    return {path.lower(): path for path in result.stdout.splitlines()}


def all_chat_paths(data_orig_dir):
    for dir_path, dir_names, file_names in os.walk(data_orig_dir, True):
        if '.git' in dir_names:
            dir_names.remove('.git')
        for file_name in file_names:
            if file_name.endswith('.cha'):
                yield os.path.join(dir_path, file_name)


def all_media_errors(data_orig_dir, media_root_dir, media_dict):
    """
    Check media files for each CHAT file to make sure they exist in the right place.
    Yield
    TODO Could do in parallel using multiprocessing.
    """
    for chat_path in all_chat_paths(data_orig_dir):
        # Read whole file.
        # TODO Recover from file read failure.
        with open(chat_path, encoding='utf-8') as f:
            text = f.read()
            relative_chat_path = chat_path.lstrip(data_orig_dir)
            yield chat_doc_errors(relative_chat_path, text, media_root_dir, media_dict)


def chat_doc_errors(relative_chat_path, text, media_root_dir, media_dict):
    """
    Check a single CHAT file, return list of errors found, [] if none.
    """
    media_infos = parse_chat_doc_medias(text)

    errors = []
    for media_type, name in media_infos:
        if media_type == 'audio':
            file = name + '.mp3'
        elif media_type == 'video':
            file = name + '.mp4'
        elif media_type == 'pic':
            # Extension was included.
            file = name
        else:
            errors.append(('impossible media type', media_type, name))
            continue

        relative_chat_dir = os.path.dirname(relative_chat_path)
        path = os.path.join(media_root_dir, relative_chat_dir, file)
        lower_path = path.lower()
        actual_path = media_dict.get(lower_path)
        if actual_path:
            if path != actual_path:
                errors.append((f'incorrectly-cased {actual_path}', media_type, path))
        else:
            errors.append(('missing', media_type, path))

    return errors


def parse_chat_doc_medias(text):
    """
    Return list of video, audio, pic information.
    """
    av = av_expected(text)
    pics = [('pic', file_name) for file_name in pic_expected(text)]
    if av:
        pics.append(av)
        return pics
    else:
        return pics


def av_expected(text):
    """
    Return media type and name expected, or None.

    >>> av_expected('@Media:\\tname, video\\n')
    ('video', 'name')
    """
    match = re.search(media_re, text)
    if match:
        if match.group(3):
            return None
        else:
            return (match.group(2), match.group(1))
    else:
        return None


def pic_expected(text):
    """
    Return list of file names.

    >>> pic_expected('%pic:"foo.jpg" junk %pic:"bar.gif"')
    ['foo.jpg', 'bar.gif']
    >>> pic_expected('nothing')
    []
    """
    return re.findall(pic_re, text)


if __name__ == '__main__':
    main()
