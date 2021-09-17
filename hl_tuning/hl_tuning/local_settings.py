import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-5=40eqoq&mhxr2qy7wj+y8)l8@2&!8aoht8k0*bgryjr#8+60n'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.sqlite3",
        'NAME': 'hltuning',
        'USER': 'htun',
        'PASSWORD': 'htun',
        'HOST': 'localhost',
        'PORT': '5432'
        }
}

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]