from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status

from allauth.account.views import SignupView, ConfirmEmailView
from allauth.account.utils import complete_signup
from allauth.account import app_settings

from rest_auth.app_settings import (
    UserDetailsSerializer,
    TokenSerializer,
)
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.views import (
    Login,
    EverybodyCanAuthentication,
)


class Register(APIView, SignupView):
    """
    Accepts the credentials and creates a new user
    if user does not exist already
    Return the REST Token and the user object
    if the credentials are valid and authenticated.
    Calls allauth complete_signup method

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key
    and user object.
    """

    permission_classes = (AllowAny,)
    authentication_classes = (EverybodyCanAuthentication,)
    token_model = Token
    token_serializer = TokenSerializer
    user_serializer_class = UserDetailsSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def form_valid(self, form):
        self.user = form.save(self.request)
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if isinstance(self.request, HttpRequest):
            request = self.request
        else:
            request = self.request._request
        return complete_signup(request, self.user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.initial = {}
        self.request.POST = self.request.DATA.copy()
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form_valid(self.form)
            return self.get_response()
        else:
            return self.get_response_with_errors()

    def get_response(self):
        response = self.token_serializer(self.token).data
        user = self.user_serializer_class(instance=self.user).data
        response['user'] = user
        return Response(response, status=status.HTTP_201_CREATED)

    def get_response_with_errors(self):
        return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView, ConfirmEmailView):

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['key'] = self.request.DATA.get('key', '')
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class SocialLogin(Login):
    """
    class used for social authentications
    example usage for facebook with access_token

    -------------
    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

    class FacebookLogin(SocialLogin):
        adapter_class = FacebookOAuth2Adapter

    -------------
    example usage for facebook with code

    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client

    class FacebookLogin(SocialLogin):
        adapter_class = FacebookOAuth2Adapter
        client_class = OAuth2Client
        callback_url = 'localhost:8000'
    -------------
    """

    serializer_class = SocialLoginSerializer
