"""
Django settings for bla project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import bla.settings_secret as settings_secret

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = settings_secret.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blabla',
    'django_jinja',
    'sslserver',    # only for testing
    'ws4redis',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bla.urls'

# This setting is required to override the Django's main loop, when running in
# development mode, such as ./manage runserver
WSGI_APPLICATION = 'ws4redis.django_runserver.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.static',
            'ws4redis.context_processors.default',
            'django.template.context_processors.request',
        ],
        'loaders': [
            'django_jinja.loaders.AppLoader',
            'django_jinja.loaders.FileSystemLoader',
            'django.template.loaders.app_directories.Loader',
        ],
    },
}]

# Security stuff

# SecurityMiddleware redirects all non-HTTPS requests to HTTPS (except for those URLs matching a regular
# expression listed in SECURE_REDIRECT_EXEMPT).
SECURE_SSL_REDIRECT = True
# Use a secure cookie for the session cookie
SESSION_COOKIE_SECURE = True
# Use a secure cookie for the CSRF cookie
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
# Set the HTTP Strict Transport Security header on all responses that do not already have it.
# When enabling HSTS, it's a good idea to first use a small value for testing, for example, SECURE_HSTS_SECONDS = 3600
# for one hour. Each time a Web browser sees the HSTS header from your site, it will refuse to communicate non-securely
# (using HTTP) with your domain for the given period of time. Once you confirm that all assets are served securely on
# your site (i.e. HSTS didn't break anything), it's a good idea to increase this value so that infrequent visitors will
# be protected (31536000 seconds, i.e. 1 year, is common).
SECURE_HSTS_SECONDS = 3600
# Do I want this or not?
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Websocket Redis stuff
WEBSOCKET_URL = '/ws/'
WS4REDIS_EXPIRE = 7200
WS4REDIS_HEARTBEAT = "--heartbeat--"

# This directive is required during development and ignored in production environments.
# It overrides Django's internal main loop and adds a URL dispatcher in front of the request handler
WSGI_APPLICATION = 'ws4redis.django_runserver.application'

os.environ['wsgi.url_scheme'] = 'https'

# For django.middleware.clickjacking.XFrameOptionsMiddleware, default is "SAMEORIGIN"
X_FRAME_OPTIONS = "DENY"






