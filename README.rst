Check CHAT media files for existence
====================================

|Build Status|

What it does
------------

``check_chat_media`` looks at all media references in CHAT files and checks to see whether they exist on the specified media server, reporting everything that is missing.

Prerequisites
-------------

Make sure to have Python 3 installed, e.g., on macOS, you can use
Homebrew with

::

    $ brew install python3

Install
-------

Clone this repo and ``cd`` into it, then run

::

    $ python3 setup.py install

to install the executable ``check_chat_media``.

Usage
-----

::

    $ check_chat_media --chatdir ./talkbank-data --host talkbank.org --mediadir /TalkBank/media

::

    Options:
        --chatdir TEXT   CHAT root dir  [required]
        --host TEXT      Host name of media  [required]
        --mediadir TEXT  Media root dir on host  [required]
        --help           Show this message and exit.

.. |Build Status| image:: https://travis-ci.org/TalkBank/check_chat_media.png
   :target: https://travis-ci.org/TalkBank/check_chat_media
