import logging
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])


logging.disable(logging.CRITICAL)
ROOT_URLCONF = 'urls'
STATIC_URL = '/static/'
STATIC_ROOT = '%s/staticserve' % PROJECT_ROOT
STATICFILES_DIRS = (
    ('global', '%s/static' % PROJECT_ROOT),
)
UPLOADS_DIR_NAME = 'uploads'
MEDIA_URL = '/%s/' % UPLOADS_DIR_NAME
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '%s' % UPLOADS_DIR_NAME)

IS_DEV = False
IS_STAGING = False
IS_PROD = False
IS_TEST = 'test' in sys.argv or 'test_coverage' in sys.argv

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
]

# Adding for backwards compatibility for Django 1.8 tests
MIDDLEWARE_CLASSES = MIDDLEWARE

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',

    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
]

# avoid deprecation warnings during tests
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )
}

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = 'test-results'

INSTALLED_APPS = [
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',

    'rest_framework',
    'rest_framework.authtoken',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'rest_framework_simplejwt.token_blacklist'
]

SECRET_KEY = "38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd"
ACCOUNT_ACTIVATION_DAYS = 1
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
