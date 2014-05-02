import django
import os, sys

# PROJECT_ROOT = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])
# sys.path.append(os.path.join(PROJECT_ROOT, 'django-rest-registration-auth/apps/'))
# ROOT_URLCONF = 'urls'

# STATIC_URL = '/static/'
# STATIC_ROOT = '%s/staticserve' % PROJECT_ROOT
# STATICFILES_DIRS = (
#     ('global', '%s/static' % PROJECT_ROOT),
# )
# UPLOADS_DIR_NAME = 'uploads'
# MEDIA_URL = '/%s/' % UPLOADS_DIR_NAME
# MEDIA_ROOT = os.path.join(PROJECT_ROOT, '%s' % UPLOADS_DIR_NAME)

IS_DEV = False
IS_STAGING = False
IS_PROD = False
IS_TEST = 'test' in sys.argv

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
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'rest_framework',
    'rest_framework.authtoken',
    'registration',

    'rest_auth',
]

SECRET_KEY = "38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd"


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    newsletter_subscribe = models.BooleanField(default=False)

    class Meta:
        app_label = 'rest_auth'

REST_PROFILE_MODULE = UserProfile
REST_REGISTRATION_BACKEND = 'registration.backends.default.views.RegistrationView'
ACCOUNT_ACTIVATION_DAYS = 1
