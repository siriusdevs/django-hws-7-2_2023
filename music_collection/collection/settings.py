from pathlib import Path
from dotenv import load_dotenv
from os import getenv, path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.dirname(os.path.abspath(__file__))


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/audio_files'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_ea@n&rnx3^8p2l!!juw_)6wvc%+y&q&64#0bmfvd^j56o0)kj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

APPEND_SLASH=False

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'collection_app',
    'rest_framework',
    'rest_framework.authtoken',
]
# Понять, какую из аутентификация будем использовать
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'collection.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'collection.wsgi.application'

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('PG_DBNAME'),
        'USER': getenv('PG_USER'),
        'PASSWORD': getenv('PG_PASSWORD'),
        'HOST': getenv('PG_HOST'),
        'PORT': getenv('PG_PORT'),
        'OPTIONS': {
            'options': '-c search_path=public,collection'
        },
        'TEST': {
            'NAME': 'test'
        }
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Параметры интернационализации и локализации

# Internationalization
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True # Логическое значение, указывающее, включена ли система перевода Джанго. По умолчанию это значение True.

USE_TZ = True # Логическое значение, указывающее, являются ли datetimes известными часовыми поясами. При создании проекта с командой startproject это значение равно True

LOCALE_PATH = 'collection_app/locale' 

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # При запуске новых проектов в Django 3.2 типом по умолчанию для первичных ключей установлено значение a, BigAutoFieldпредставляющее собой 64-битное целое число

TEST_RUNNER = 'tests.runner.PostgresSchemaRunner'
