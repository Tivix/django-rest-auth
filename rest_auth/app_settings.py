from django.conf import settings

from rest_auth.serializers import (
    TokenSerializer as DefaultTokenSerializer,
    JWTSerializer as DefaultJWTSerializer,
    UserDetailsSerializer as DefaultUserDetailsSerializer,
    LoginSerializer as DefaultLoginSerializer,
    PasswordResetSerializer as DefaultPasswordResetSerializer,
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
    PasswordChangeSerializer as DefaultPasswordChangeSerializer)
from .utils import import_callable, default_create_token

create_token = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token))

serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

TokenSerializer = import_callable(
    serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))

JWTSerializer = import_callable(
    serializers.get('JWT_SERIALIZER', DefaultJWTSerializer))

UserDetailsSerializer = import_callable(
    serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)
)

LoginSerializer = import_callable(
    serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)
)

PasswordResetSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_SERIALIZER',
        DefaultPasswordResetSerializer
    )
)

PasswordResetConfirmSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_CONFIRM_SERIALIZER',
        DefaultPasswordResetConfirmSerializer
    )
)

PasswordChangeSerializer = import_callable(
    serializers.get(
        'PASSWORD_CHANGE_SERIALIZER',
        DefaultPasswordChangeSerializer
    )
)
