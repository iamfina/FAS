#!/usr/bin/env python

import json
from os import environ as _e
from distutils.core import setup

CREDENTIALS_FILE = './credentials.json'

with open(CREDENTIALS_FILE, 'w') as f:
    json.dump(dict(
        user=_e.get('POSTGRES_USER', ''),
        password=_e.get('POSTGRES_PASSWORD', ''),
        host=_e.get('POSTGRES_HOST', 'localhost'),
        database=_e.get('POSTGRES_DB', ''),
        port=_e.get('POSTGRES_PORT', 5432)
    ), f)


setup(
    name='pp_models',
    version='0.1.0',
    py_modules=['readers'],
    data_files=[('', [CREDENTIALS_FILE])]
)
