from setuptools import setup, find_packages
setup(
    name='check_chat_media',
    version='1.0',
    py_modules=['check_chat_media'],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': ['check_chat_media=check_chat_media:main'],
    },
    author='Franklin Chen',
    author_email='franklinchen@franklinchen.com',
    description='Check CHAT media files for existence',
    license='BSD',
    keywords='parse',
    url='https://github.com/TalkBank/check_chat_media',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
