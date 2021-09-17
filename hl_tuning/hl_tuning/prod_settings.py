import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-5=40eqoq&mhxr2qy7wj+y8)l777&!8aoht8k0*bgryjr#8+60n'


DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': 'hltuning',
        'USER': 'htuning',
        'PASSWORD': 'htuning',
        'HOST': 'localhost',
        'PORT': '5432'
        }
}

import os

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')