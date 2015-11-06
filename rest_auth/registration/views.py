from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from allauth.account.views import SignupView, ConfirmEmailView
from allauth.account.utils import complete_signup
from allauth.account import app_settings

from rest_auth.app_settings import TokenSerializer
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.views import LoginView


class RegisterView(APIView, SignupView):
    """
    Accepts the credentials and creates a new user
    if user does not exist already
    Return the REST Token if the credentials are valid and authenticated.
    Calls allauth complete_signup method

    Accept the following POST parameters: username, email, password
    Return the REST Framework Token Object's key.
    """

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    token_model = Token
    serializer_class = TokenSerializer

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def form_valid(self, form):
        self.user = form.save(self.request)
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user
        )
        if isinstance(self.request, HttpRequest):
            request = self.request
        else:
            request = self.request._request
        return complete_signup(request, self.user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RegisterView, self).get_form_kwargs(*args, **kwargs)
        kwargs['data'] = self.request.data
        return kwargs

    def post(self, request, *args, **kwargs):
        self.initial = {}
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form_valid(self.form)
            return self.get_response()
        else:
            return self.get_response_with_errors()

    def get_response(self):
        # serializer = self.user_serializer_class(instance=self.user)
        serializer = self.serializer_class(instance=self.token,
                                           context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_response_with_errors(self):
        return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView, ConfirmEmailView):

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['key'] = self.request.data.get('key', '')
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class SocialLoginView(LoginView):
    """
    class used for social authentications
    example usage for facebook with access_token
    -------------
    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

    class FacebookLogin(SocialLoginView):
        adapter_class = FacebookOAuth2Adapter
    -------------

    example usage for facebook with code

    -------------
    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client

    class FacebookLogin(SocialLoginView):
        adapter_class = FacebookOAuth2Adapter
         client_class = OAuth2Client
         callback_url = 'localhost:8000'
    -------------
    """

    serializer_class = SocialLoginSerializer
