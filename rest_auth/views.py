from django.contrib.auth import login, logout
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication

from .app_settings import (
    TokenSerializer,
    UserDetailsSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
)


# http://bytefilia.com/titanium-mobile-facebook-application-django-allauth-sign-sign/
class EverybodyCanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        return None


class Login(GenericAPIView):
    """
    Check the credentials and return the REST Token
    and the user object
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key
    and user object.
    """

    permission_classes = (AllowAny,)
    authentication_classes = (EverybodyCanAuthentication,)
    serializer_class = LoginSerializer
    token_model = Token
    response_serializer = TokenSerializer
    user_serializer = UserDetailsSerializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        response = self.response_serializer(self.token).data
        user = self.user_serializer(instance=self.user).data
        response['user'] = user
        return Response(
            response,
            status=status.HTTP_200_OK
        )

    def get_error_response(self):
        return Response(
            self.serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.DATA)
        if not self.serializer.is_valid():
            return self.get_error_response()
        self.login()
        return self.get_response()


class Logout(APIView):

    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)
    authentication_classes = (EverybodyCanAuthentication,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)

        return Response(
            {"success": "Successfully logged out."},
            status=status.HTTP_200_OK
        )


class UserDetails(RetrieveUpdateAPIView):

    """
    Returns User's details in JSON format.

    Accepts the following GET parameters: token
    Accepts the following POST parameters:
        Required: token
        Optional: email, first_name, last_name and UserProfile fields
    Returns the updated UserProfile and/or User object.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (EverybodyCanAuthentication,)

    def get_object(self):
        return self.request.user


class PasswordReset(GenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (EverybodyCanAuthentication,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.DATA
        serializer = self.get_serializer(data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"success": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirm(GenericAPIView):

    """
    Password reset e-mail link is confirmed,
    therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (EverybodyCanAuthentication,)

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {"success": "Password has been reset with the new password."}
        )


class PasswordChange(GenericAPIView):

    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (EverybodyCanAuthentication,)

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {"success": "New password has been saved."}
        )
