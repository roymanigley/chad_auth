"""
Django settings for chad_auth project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from os import path
from pathlib import Path

from chad_auth_oidc.oidc_helper.keys import Util as key_util

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

OIDC_BASE_URL = os.getenv('CHAD_AUTH_OIDC_BASE_URL', f'http://localhost:{8000}')
OIDC_ACCESS_TOKEN_LIFE_TIME_SECONDS = int(os.getenv('CHAD_AUTH_OIDC_ACCESS_TOKEN_LIFE_TIME_SECONDS', 60 * 15))
OIDC_SESSION_LIFE_TIME_SECONDS = int(os.getenv('CHAD_AUTH_OIDC_SESSION_LIFE_TIME_SECONDS', 60 * 60 * 8))
KEYS_BASE_DIR = os.getenv('CHAD_AUTH_KEYS_BASE_DIR', BASE_DIR)
CHAD_AUTH_ALLOWED_HOSTS = os.getenv('CHAD_AUTH_ALLOWED_HOSTS', 'localhost 127.0.0.1 0.0.0.0').split(' ')
CHAD_AUTH_SECRET_KEY = os.getenv('CHAD_AUTH_SECRET_KEY', 'django-insecure--u3cs@48xwfvf4acy@jq#r$u)6uq7wn0u-8h3j%pl##8ks4&h^').split(' ')
CHAD_AUTH_APP_PROFILE = os.getenv('CHAD_AUTH_APP_PROFILE')
CHAD_AUTH_SQLITE_PATH = os.getenv('CHAD_AUTH_SQLITE_PATH', BASE_DIR / 'db.sqlite3')

key_util.init_keys(KEYS_BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CHAD_AUTH_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CHAD_AUTH_APP_PROFILE != 'PROD'

ALLOWED_HOSTS = CHAD_AUTH_ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chad_auth_api',
    'chad_auth_oidc',
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

ROOT_URLCONF = 'chad_auth.urls'

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

WSGI_APPLICATION = 'chad_auth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': CHAD_AUTH_SQLITE_PATH,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
