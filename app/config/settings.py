"""
Django settings for summary_generator project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-m(ddoo2t@(j5r615&y$r$(dr9t0@gi@-a9iz@qvfp95k$%x*41")

DEBUG = SECRET_KEY = os.environ.get("DEBUG", "True")

ALLOWED_HOSTS = ['*']

# Application definition


INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_results',
    'django_celery_beat',
    'applogger',
    'mymodule',
]

RMQ_IP=os.environ.get("DEBUG", "192.168.1.101")
CELERY_BROKER_URL=os.environ.get("DEBUG", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND='django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = [os.environ.get("URL_API_HOST", "http://192.168.0.153:2000")]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',

        ],
    },
},
]

SITE_ID = 1
WSGI_APPLICATION = 'config.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'errorformatter': {
            'format': '{levelname} {asctime} {process:d} {thread:d} \n {message}',
            'style': '{'
        },
        "only_message": {
            "format": "{message}",
            "style": "{",
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'log.log',
            'formatter': 'errorformatter'
        },
        'db': {
            'level': 'INFO',
            "class": "applogger.handlers.DBHandler",
            "model": "applogger.models.LogEntry",
            "expiry": 86400,
            "formatter": "only_message",
        },
    },
    'loggers': {
        'jobs': {
            'handlers': ['file',],
            'level': 'WARNING',
            'propagate': True,

        },
        'core': {
            'handlers': ['file', 'db'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

"""
CREATE DATABASE summary;
CREATE USER django WITH PASSWORD 'django';
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE summary TO django;
GRANT ALL ON schema public TO django;

зайти непосредсвенно в summary bd если не работает миграция
"""
# миграции в контейнере ------ docker-compose exec web python manage.py migrate --noinput 
# проверяем бд --------------- docker-compose exec db psql --username=django --dbname=summary
# ---------------------------- \l ; CTc/django ; \c ; \dt ;  \q;
# провверяем создание тома --- docker volume inspect  APP_NAME_postgres_data

# для прода надо статику собрать-- docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear 

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": os.environ.get("SQL_DATABASE", "summary"),
        "USER": os.environ.get("SQL_USER", "django"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "django"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_REFERRER_POLICY = None
X_FRAME_OPTIONS = 'ALLOWALL'


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'