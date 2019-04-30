from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost']

INSTALLED_APPS += []


TEMPLATES_DEVELOPMENT_SETTINGS = {
    'string_if_invalid': 'INVALID: %s',
    'debug': DEBUG
}

TEMPLATES[0]['OPTIONS'].update(TEMPLATES_DEVELOPMENT_SETTINGS)
