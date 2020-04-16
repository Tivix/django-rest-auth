from django.conf import settings
from django.utils.module_loading import import_string

TokenModel = import_string(getattr(settings, 'REST_AUTH_TOKEN_MODEL', 'rest_framework.authtoken.models.Token'))
