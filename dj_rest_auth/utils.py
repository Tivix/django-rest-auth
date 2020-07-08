from importlib import import_module

from django.conf import settings


def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, str)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def default_create_token(token_model, user, serializer):
    token, _ = token_model.objects.get_or_create(user=user)
    return token


def jwt_encode(user):
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

    JWTTokenClaimsSerializer = rest_auth_serializers.get(
        'JWT_TOKEN_CLAIMS_SERIALIZER',
        TokenObtainPairSerializer
    )

    TOPS = import_callable(JWTTokenClaimsSerializer)
    refresh = TOPS.get_token(user)
    return refresh.access_token, refresh


try:
    from .jwt_auth import JWTCookieAuthentication
except ImportError:
    pass
