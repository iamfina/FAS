#!/usr/bin/env python

from distutils.core import setup


install_requires = [
    "pony>=0.7.3",
    "psycopg2-binary>=2.7.5"
]

setup(
    name='Project procurement',
    version='0.1.0',
    description='Project procurement models',
    author='Sergey Emelyanov',
    author_email='karagabul@gmail.com',
    packages=[],
    install_requires=install_requires
 )
