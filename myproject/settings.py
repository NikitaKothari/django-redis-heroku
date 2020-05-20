"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku

def get_int_env(varname, default=None):
    value = os.environ.get(varname)
    if value is None:
        return default

    return int(value)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hl%k-il8!3(3-%(lmgw6861!qm4g+#3ri1ovb4f&%ocvhou6%o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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
WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# REDIS CONFIG
REDIS_URL = os.environ.get('REDISCLOUD_URL', 'redis://127.0.0.1:6379')
BROKER_URL = os.environ.get('HEROKU_REDIS_BLACK_URL', 'redis://127.0.0.1:6379')
BROKER_CONNECTION_MAX_RETRIES = os.environ.get('BROKER_CONNECTION_MAX_RETRIES', None)
BROKER_POOL_LIMIT = os.environ.get('BROKER_POOL_LIMIT', 10)

# CELERY CONFIG
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', BROKER_URL)
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', BROKER_URL)
CELERY_REDIS_MAX_CONNECTIONS = os.environ.get('CELERY_REDIS_MAX_CONNECTIONS', 10)

LIMIT = get_int_env('LIMIT', 5)
LIMIT1 = get_int_env('LIMIT', 5)

CACHE_URL = os.environ.get("CACHE_URL", REDIS_URL)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHE_URL,
        "OPTIONS": {
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': get_int_env('LIMIT', 5),
                'timeout': 20,
            },
            'MAX_CONNECTIONS': get_int_env('LIMIT1', 1000),
        },
        "VERSION": 1,
    }
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True


# Configure Django App for Heroku.
django_heroku.settings(locals())
