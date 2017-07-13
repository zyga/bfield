#!/usr/bin/env python
"""
Setup / installer for zk-bitfield.

:author: Zygmunt Krynicki <me@zygoon.pl>
:copyright: Copyright (c) 2017 Zygmunt Krynicki.
:license: MIT
"""
from setuptools import setup  # type: ignore

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development',
]

setup(
    name='bfield',
    version='0.9',
    author='Zygmunt Krynicki',
    author_email='me@zygoon.pl',
    description="Convenient bit fields for int subclasses",
    license='MIT',
    py_modules=['bfield'],
    test_suite='test_bfield',
    classifiers=classifiers,
)
