from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck

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
