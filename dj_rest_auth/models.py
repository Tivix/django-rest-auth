from django.conf import settings
from rest_framework.authtoken.models import Token as DefaultTokenModel

# Register your models here.

TokenModel = getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel)
