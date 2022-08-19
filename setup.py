#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from textwrap import dedent

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]


setup(
    name="ffmpeg",
    packages=["ffmpeg"],
    version="1.0.2",
    author="Taeyelor",
    author_email="taeyelor@gmail.com",
    url="https://github.com/taeyelor/py-ffmpeg",
    keywords="ffmpeg",
    description="FFmpeg wrapper for Python",
    long_description=dedent(r"""\
     FFmpeg wrapper for Python
        """),
    python_requires=">=3.7",
    install_requires=requires
)
