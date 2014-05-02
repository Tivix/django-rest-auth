import django

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
    'rest_auth',
]

SECRET_KEY = "38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd"
