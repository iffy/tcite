#!/usr/bin/env python
# Copyright (c) Matt Haggard
# See LICENSE for details.


from distutils.core import setup

setup(
    name='tcite',
    version='0.1.0',
    description='Python library for using tcite notation',
    author='Matt Haggard',
    author_email='haggardii@gmail.com',
    url='https://github.com/iffy/tcite',
    install_requires=[
        'parsley',
    ],
    packages=[
        'tcite', 'tcite.test',
    ],
)