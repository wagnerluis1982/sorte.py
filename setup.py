# encoding=utf8

import codecs
from setuptools import setup, find_packages

PACKAGE_DIR = 'src'

setup(
    name = "sorte.py",
    version = "0.0.5",
    author = "Wagner Macedo",
    author_email = "wagnerluis1982@gmail.com",
    description = "Geração e conferência de apostas de loterias",
    long_description = codecs.open("README", 'r', encoding='utf-8').read(),
    license = "GPL",
    url = "https://github.com/wagnerluis1982/sorte-py",
    package_dir = {'': PACKAGE_DIR},
    packages = find_packages(PACKAGE_DIR),
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
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Other/Nonlisted Topic",
    ],
)
