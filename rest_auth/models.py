from django.conf import settings

if getattr(settings, 'REST_AUTH_TOKEN_APP', False) is 'knox':
    try:
        from knox.models import AuthToken as DefaultTokenModel
    except ImportError:
        raise ImportError("Install django-rest-knox before setting REST_AUTH_TOKEN_APP to 'knox'")
else:
    from rest_framework.authtoken.models import Token as DefaultTokenModel

from .utils import import_callable

# Register your models here.

TokenModel = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))
