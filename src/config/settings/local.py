from config.settings.base import *

DEBUG = True

INSTALLED_APPS += [
    'silk',
    'django_extensions',
]

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
]