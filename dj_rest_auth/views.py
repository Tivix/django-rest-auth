from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .app_settings import (JWTSerializer, LoginSerializer,
                           PasswordChangeSerializer,
                           PasswordResetConfirmSerializer,
                           PasswordResetSerializer, TokenSerializer,
                           UserDetailsSerializer, create_token)
from .models import TokenModel
from .utils import jwt_encode

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel
    throttle_scope = 'dj_rest_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.access_token, self.refresh_token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token
            }
            serializer = serializer_class(instance=data,
                                          context=self.get_serializer_context())
        else:
            serializer = serializer_class(instance=self.token,
                                          context=self.get_serializer_context())

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
            cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
            cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
            cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')
            from rest_framework_simplejwt.settings import api_settings as jwt_settings
            if cookie_name:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.ACCESS_TOKEN_LIFETIME)
                response.set_cookie(
                    cookie_name,
                    self.access_token,
                    expires=expiration,
                    secure=cookie_secure,
                    httponly=cookie_httponly,
                    samesite=cookie_samesite
                )
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)

        if getattr(settings, 'REST_USE_JWT', False):
            # NOTE: this import occurs here rather than at the top level
            # because JWT support is optional, and if `REST_USE_JWT` isn't
            # True we shouldn't need the dependency
            from rest_framework_simplejwt.exceptions import TokenError
            from rest_framework_simplejwt.tokens import RefreshToken

            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
            if cookie_name:
                response.delete_cookie(cookie_name)

            elif 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
                # add refresh token to blacklist
                try:
                    token = RefreshToken(request.data['refresh'])
                    token.blacklist()

                except KeyError:
                    response = Response({"detail": _("Refresh token was not included in request data.")},
                                        status=status.HTTP_401_UNAUTHORIZED)

                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, 'args'):
                        if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                            response = Response({"detail": _(error.args[0])},
                                                status=status.HTTP_401_UNAUTHORIZED)

                        else:
                            response = Response({"detail": _("An error has occurred.")},
                                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    else:
                        response = Response({"detail": _("An error has occurred.")},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                response = Response({
                    "detail": _("Neither cookies or blacklist are enabled, so the token has not been deleted server "
                                "side. Please make sure the token is deleted client side."
                                )}, status=status.HTTP_200_OK)

        return response


class UserDetailsView(RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        """
        return get_user_model().objects.none()


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    throttle_scope = 'dj_rest_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})
