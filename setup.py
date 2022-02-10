# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="kamtubepy",
    version="0.0.1",
    description="youtube downloader",
    license="MIT",
    author="kamuridesu",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ]
)
