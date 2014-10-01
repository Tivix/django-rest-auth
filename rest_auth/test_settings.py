import django
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])
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

if django.VERSION[:2] >= (1, 3):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASE_ENGINE = 'sqlite3'

INSTALLED_APPS = [
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

    'rest_framework',
    'rest_framework.authtoken',

    'rest_auth',
    'rest_auth.registration'
]

SECRET_KEY = "38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd"
ACCOUNT_ACTIVATION_DAYS = 1
SITE_ID = 1
