from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
try:
    from django.utils.http import urlsafe_base64_decode as uid_decoder
except:
    # make compatible with django 1.5
    from django.utils.http import base36_to_int as uid_decoder
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import _resolve_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_auth.utils import construct_modules_and_import
from rest_auth.serializers import (TokenSerializer, UserDetailsSerializer,
    LoginSerializer,
    SetPasswordSerializer, PasswordResetSerializer, UserUpdateSerializer,
    get_user_profile_serializer, get_user_profile_update_serializer)


def get_user_profile_model():
    # Get the UserProfile model from the setting value
    user_profile_path = getattr(settings, 'REST_PROFILE_MODULE', None)
    if user_profile_path:
        setattr(settings, 'AUTH_PROFILE_MODULE', user_profile_path)
        return _resolve_model(user_profile_path)


class LoggedInRESTAPIView(APIView):
    authentication_classes = ((SessionAuthentication, TokenAuthentication))
    permission_classes = ((IsAuthenticated,))


class LoggedOutRESTAPIView(APIView):
    permission_classes = ((AllowAny,))


class Login(LoggedOutRESTAPIView, GenericAPIView):

    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """

    serializer_class = LoginSerializer
    token_model = Token
    token_serializer = TokenSerializer

    def post(self, request):
        # Create a serializer with request.DATA
        serializer = self.serializer_class(data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        user = serializer.object['user']
        token, created = self.token_model.objects.get_or_create(user=user)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(request, user)

        return Response(self.token_serializer(token).data,
                        status=status.HTTP_200_OK)


class Logout(LoggedInRESTAPIView):

    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class UserDetails(LoggedInRESTAPIView, GenericAPIView):

    """
    Returns User's details in JSON format.

    Accepts the following GET parameters: token
    Accepts the following POST parameters:
        Required: token
        Optional: email, first_name, last_name and UserProfile fields
    Returns the updated UserProfile and/or User object.
    """
    if get_user_profile_model():
        serializer_class = get_user_profile_update_serializer()
    else:
        serializer_class = UserUpdateSerializer

    def get_profile_serializer_class(self):
        return get_user_profile_serializer()

    def get_profile_update_serializer_class(self):
        return get_user_profile_update_serializer()

    def get(self, request):
        # Create serializers with request.user and profile
        user_profile_model = get_user_profile_model()
        if user_profile_model:
            profile_serializer_class = self.get_profile_serializer_class()
            serializer = profile_serializer_class(request.user.get_profile())
        else:
            serializer = UserDetailsSerializer(request.user)
        # Send the Return the User and its profile model with OK HTTP status
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the User object updater via this Serializer
        user_profile_model = get_user_profile_model()
        if user_profile_model:
            profile_serializer_class = self.get_profile_update_serializer_class()
            serializer = profile_serializer_class(request.user.get_profile(),
                data=request.DATA, partial=True)
        else:
            serializer = UserUpdateSerializer(request.user, data=request.DATA,
                partial=True)

        if serializer.is_valid():
            # Save UserProfileUpdateSerializer
            serializer.save()

            # Return the User object with OK HTTP status
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Return the UserProfileUpdateSerializer errors with Bad Request
            # HTTP status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(LoggedOutRESTAPIView, GenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    password_reset_form_class = PasswordResetForm

    def post(self, request):
        # Create a serializer with request.DATA
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            # Create PasswordResetForm with the serializer
            reset_form = self.password_reset_form_class(data=serializer.data)

            if reset_form.is_valid():
                # Sett some values to trigger the send_email method.
                opts = {
                    'use_https': request.is_secure(),
                    'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
                    'request': request,
                }

                reset_form.save(**opts)

                # Return the success message with OK HTTP status
                return Response(
                    {"success": "Password reset e-mail has been sent."},
                    status=status.HTTP_200_OK)

            else:
                return Response(reset_form._errors,
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm(LoggedOutRESTAPIView, GenericAPIView):

    """
    Password reset e-mail link is confirmed, therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """

    serializer_class = SetPasswordSerializer

    def post(self, request, uid=None, token=None):
        # Get the UserModel
        UserModel = get_user_model()

        # Decode the uidb64 to uid to get User object
        try:
            uid = uid_decoder(uid)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        # If we get the User object
        if user:
            serializer = self.serializer_class(data=request.DATA, user=user)

            if serializer.is_valid():
                # Construct SetPasswordForm instance
                form = SetPasswordForm(user=user, data=serializer.data)

                if form.is_valid():
                    if default_token_generator.check_token(user, token):
                        form.save()

                        # Return the success message with OK HTTP status
                        return Response(
                            {"success":
                                "Password has been reset with the new password."},
                            status=status.HTTP_200_OK)
                    else:
                        return Response(
                            {"error": "Invalid password reset token."},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(form._errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"errors": "Couldn\'t find the user from uid."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(LoggedInRESTAPIView, GenericAPIView):

    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = SetPasswordSerializer

    def post(self, request):
        # Create a serializer with request.DATA
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            # Construct the SetPasswordForm instance
            form = SetPasswordForm(user=request.user, data=serializer.data)

            if form.is_valid():
                form.save()

                # Return the success message with OK HTTP status
                return Response({"success": "New password has been saved."},
                                status=status.HTTP_200_OK)

            else:
                return Response(form._errors,
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
