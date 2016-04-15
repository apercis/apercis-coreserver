#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='opinator',
    packages=['opinator'],
    version='0.1',
    description='Get review summary/sentiment',
    author='TheLateLatif',
    keywords=['reviews', 'sentiment', 'summary'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',

    ],
    include_package_data=True,
    install_requires=read('requirements.txt'),
)
