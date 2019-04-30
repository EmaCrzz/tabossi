# coding=utf-8

from .base import *

# Este archivo no debe renombrarse, se debe hacer una copia local como local.py (o crear
# un archivo nuevo en este directorio) y no agregarlo a Mercurial.
# local.py esta configurado para ser ignorado, via .hgignore

"""
Configuración personalizada de cada developer.

"""
DEBUG = True
ALLOWED_HOSTS = ['*']
DB_NAME = 'tabossi'
DB_TEST = '/'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,      # Or path to database file if using sqlite3.
        'USER': 'admin',     # Not used with sqlite3.
        'PASSWORD': 'admin.1234',  # Not used with sqlite3.
        'HOST': '127.0.0.1',      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',           # Set to empty string for default. Not used with sqlite3.
        'TEST': {
            'NAME': DB_TEST
        }
    }
}
