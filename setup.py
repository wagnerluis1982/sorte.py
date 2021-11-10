# encoding=utf8

import codecs
from setuptools import setup, find_packages

setup(
    name = "sorte.py",
    version = "0.1.0.dev1",
    author = "Wagner Macedo",
    author_email = "wagnerluis1982@gmail.com",
    description = "Geração e conferência de apostas de loterias",
    long_description = codecs.open("README", 'r', encoding='utf-8').read(),
    license = "GPLv3",
    url = "https://github.com/wagnerluis1982/sorte-py",
    packages = find_packages(),
    entry_points = {
        "console_scripts": [
            "sorte.py = sortepy.script:main",
        ],
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Other/Nonlisted Topic",
    ],
)
