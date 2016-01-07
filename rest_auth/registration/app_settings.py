from django.conf import settings

from rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer)
from ..utils import import_callable


serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})

RegisterSerializer = import_callable(
    serializers.get('REGISTER_SERIALIZER', DefaultRegisterSerializer))
