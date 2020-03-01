from django.conf import settings

from dj_rest_auth.serializers import (
    TokenSerializer as DefaultTokenSerializer,
    JWTSerializer as DefaultJWTSerializer,
    UserDetailsSerializer as DefaultUserDetailsSerializer,
    LoginSerializer as DefaultLoginSerializer,
    PasswordResetSerializer as DefaultPasswordResetSerializer,
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
    PasswordChangeSerializer as DefaultPasswordChangeSerializer)
from .utils import default_create_token

create_token = getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token)

serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

TokenSerializer = serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer)

JWTSerializer = serializers.get('JWT_SERIALIZER', DefaultJWTSerializer)

UserDetailsSerializer = serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)

LoginSerializer = serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)

PasswordResetSerializer = serializers.get(
        'PASSWORD_RESET_SERIALIZER',
        DefaultPasswordResetSerializer
    )

PasswordResetConfirmSerializer = serializers.get(
    'PASSWORD_RESET_CONFIRM_SERIALIZER', DefaultPasswordResetConfirmSerializer
)

PasswordChangeSerializer = serializers.get('PASSWORD_CHANGE_SERIALIZER', DefaultPasswordChangeSerializer)
