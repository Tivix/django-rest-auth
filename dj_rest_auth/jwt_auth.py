from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_refresh_view():
    """ Returns a Token Refresh CBV without a circular import """
    from rest_framework_simplejwt.settings import api_settings as jwt_settings
    from rest_framework_simplejwt.views import TokenRefreshView
    
    class RefreshViewWithCookieSupport(TokenRefreshView):
        def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)
            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
            if cookie_name and response.status_code == 200 and 'access' in response.data:
                cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
                cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
                cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')
                token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
                response.set_cookie(
                    cookie_name,
                    response.data['access'],
                    expires=token_expiration,
                    secure=cookie_secure,
                    httponly=cookie_httponly,
                    samesite=cookie_samesite,
                )

                response.data['access_token_expiration'] = token_expiration
            return response
    return RefreshViewWithCookieSupport


class JWTCookieAuthentication(JWTAuthentication):
    """
    An authentication plugin that hopefully authenticates requests through a JSON web
    token provided in a request cookie (and through the header as normal, with a
    preference to the header).
    """
    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

    def authenticate(self, request):
        cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
        header = self.get_header(request)
        if header is None:
            if cookie_name:
                raw_token = request.COOKIES.get(cookie_name)
                if getattr(settings, 'JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED', False): #True at your own risk 
                    self.enforce_csrf(request)
                elif raw_token is not None and getattr(settings, 'JWT_AUTH_COOKIE_USE_CSRF', False):
                    self.enforce_csrf(request)
            else:
                return None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
