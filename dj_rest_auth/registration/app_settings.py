from dj_rest_auth.registration.serializers import \
    RegisterSerializer as DefaultRegisterSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny

from ..utils import import_callable

serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})

RegisterSerializer = import_callable(serializers.get('REGISTER_SERIALIZER', DefaultRegisterSerializer))


def register_permission_classes():
    permission_classes = [AllowAny, ]
    for klass in getattr(settings, 'REST_AUTH_REGISTER_PERMISSION_CLASSES', tuple()):
        permission_classes.append(import_callable(klass))
    return tuple(permission_classes)
