from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
try:
    from django.utils.http import urlsafe_base64_decode as uid_decoder
except:
    # make compatible with django 1.5
    from django.utils.http import base36_to_int as uid_decoder
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import _resolve_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.authtoken.models import Token

from registration.models import RegistrationProfile
from registration import signals
from registration.views import ActivationView

from .utils import construct_modules_and_import
from .models import *
from .serializers import TokenSerializer, UserDetailsSerializer, \
    LoginSerializer, UserRegistrationSerializer, \
    UserRegistrationProfileSerializer, \
    UserProfileUpdateSerializer, SetPasswordSerializer, \
    PasswordResetSerializer


# Get the UserProfile model from the setting value
user_profile_path = getattr(settings, 'REST_PROFILE_MODULE', None)
user_profile_model = None
if user_profile_path:
    user_profile_model = _resolve_model(user_profile_path)

# Get the REST Registration Backend for django-registration
registration_backend = getattr(settings, 'REST_REGISTRATION_BACKEND',
    'registration.backends.default.views.RegistrationView')

if not registration_backend:
    raise Exception('Please configure a registration backend')

# Get the REST REGISTRATION BACKEND class from the setting value via above
# method
RESTRegistrationView = construct_modules_and_import(registration_backend)


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

        if serializer.is_valid():
            # Authenticate the credentials by grabbing Django User object
            user = authenticate(username=serializer.data['username'],
                                password=serializer.data['password'])

            if user and user.is_authenticated():
                if user.is_active:
                    # TODO: be able to configure this to either be
                    # session or token or both
                    # right now it's both.
                    login(request, user)

                    # Return REST Token object with OK HTTP status
                    token, created = self.token_model.objects.get_or_create(user=user)
                    return Response(self.token_serializer(token).data,
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'This account is disabled.'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid Username/Password.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


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


class Register(LoggedOutRESTAPIView, GenericAPIView):

    """
    Registers a new Django User object by accepting required field values.

    Accepts the following POST parameters:
        Required: username, password, email
        Optional: first_name & last_name for User object and UserProfile fields
    Returns the newly created User object including REST Framework Token key.
    """

    serializer_class = UserRegistrationSerializer
    profile_serializer_class = UserRegistrationProfileSerializer

    def post(self, request):
        # Create serializers with request.DATA
        serializer = self.serializer_class(data=request.DATA)
        profile_serializer = self.profile_serializer_class(
            data=request.DATA)

        if serializer.is_valid() and profile_serializer.is_valid():
            # Change the password key to password1 so that RESTRegistrationView
            # can accept the data
            serializer.data['password1'] = serializer.data.pop('password')

            # TODO: Make this customizable backend via settings.
            # Call RESTRegistrationView().register to create new Django User
            # and UserProfile models
            data = serializer.data.copy()
            data.update(profile_serializer.data)

            RESTRegistrationView().register(request, **data)

            # Return the User object with Created HTTP status
            return Response(UserDetailsSerializer(serializer.data).data,
                            status=status.HTTP_201_CREATED)

        else:
            return Response({
                'user': serializer.errors,
                'profile': profile_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)


class UserDetails(LoggedInRESTAPIView, GenericAPIView):

    """
    Returns User's details in JSON format.

    Accepts the following GET parameters: token
    Accepts the following POST parameters:
        Required: token
        Optional: email, first_name, last_name and UserProfile fields
    Returns the updated UserProfile and/or User object.
    """

    serializer_class = UserProfileUpdateSerializer

    def get(self, request):
        # Create serializers with request.user and profile
        user_details = UserDetailsSerializer(request.user)
        try:
            serializer = self.serializer_class(request.user.get_profile())
            profile_data = serializer.data
        except ObjectDoesNotExist:

            profile_data = {}
        # Send the Return the User and its profile model with OK HTTP status
        return Response({
            'user': user_details.data,
            'profile': profile_data},
            status=status.HTTP_200_OK)

    def post(self, request):
        # Get the User object updater via this Serializer
        serializer = self.serializer_class(
            request.user.get_profile(), data=request.DATA, partial=True)

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

    def post(self, request):
        # Create a serializer with request.DATA
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            # Create PasswordResetForm with the serializer
            reset_form = PasswordResetForm(data=serializer.data)

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


class VerifyEmail(LoggedOutRESTAPIView, GenericAPIView):

    """
    Verifies the email of the user through their activation_key.

    Accepts activation_key django argument: key from activation email.
    Returns the success/fail message.
    """

    model = RegistrationProfile

    def get(self, request, activation_key=None):
        # Get the user registration profile with the activation key
        target_user = RegistrationProfile.objects.activate_user(activation_key)

        if target_user:
            # Send the activation signal
            signals.user_activated.send(sender=ActivationView.__class__,
                                        user=target_user,
                                        request=request)

            # Return the success message with OK HTTP status
            ret_msg = "User {0}'s account was successfully activated!".format(
                target_user.username)
            return Response({"success": ret_msg}, status=status.HTTP_200_OK)

        else:
            ret_msg = "The account was not able to be activated or already activated, please contact support."
            return Response({"errors": ret_msg}, status=status.HTTP_400_BAD_REQUEST)


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
