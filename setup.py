#!/usr/bin/env python

from setuptools import setup
from buildkit import *


META = get_metadata('waitress-serve')


setup(
    name='waitress-serve',
    version=META['version'],
    description='Command-line runner for waitress',
    long_description=read('README'),
    url='https://github.com/kgaughan/waitress-serve/',
    license='MIT',
    install_requires=read_requirements('requirements.txt'),
    scripts=['waitress-serve'],
    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6'
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
    ],

    author=META['author'],
    author_email=META['email'],
)
