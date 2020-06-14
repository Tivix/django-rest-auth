from importlib import import_module


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


try:
    from django.conf import settings
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

    def jwt_encode(user):
        TOPS = getattr(settings, 'JWT_TOKEN_CLAIMS_SERIALIZER', TokenObtainPairSerializer)
        refresh = TOPS.get_token(user)
        return refresh.access_token, refresh

    class JWTCookieAuthentication(JWTAuthentication):
        """
        An authentication plugin that hopefully authenticates requests through a JSON web
        token provided in a request cookie (and through the header as normal, with a
        preference to the header).
        """
        def authenticate(self, request):
            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
            header = self.get_header(request)
            if header is None:
                if cookie_name:
                    raw_token = request.COOKIES.get(cookie_name)
                else:
                    return None
            else:
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

except ImportError:
    raise ImportError("rest-framework-simplejwt needs to be installed")
