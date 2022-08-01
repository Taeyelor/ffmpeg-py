#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from textwrap import dedent

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]



setup(
    name="ffmpeg-py",
    packages=["ffmpeg"],
    version="1.0.0",
    author="Taeyelor",
    author_email="taeyelor@gmail.com",
    url="https://github.com/taeyelor/py-ffmpeg",
    keywords="ffmpeg",
    description="FFmpeg wrapper for Python",
    long_description=dedent(r"""\
     FFmpeg wrapper for Python
        """),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Multimedia :: Video",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.7",
    install_requires=requires
)
