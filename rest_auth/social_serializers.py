from django.http import HttpRequest
from rest_framework import serializers
from requests.exceptions import HTTPError
# Import is needed only if we are using social login, in which
# case the allauth.socialaccount will be declared
try:
    from allauth.socialaccount.helpers import complete_social_login
except ImportError:
    pass

from allauth.socialaccount.models import SocialToken


class TwitterLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    token_secret = serializers.CharField(required=True)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        """

        :param adapter: allauth.socialaccount Adapter subclass. Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :return: :return: A populated instance of the `allauth.socialaccount.SocialLoginView` instance
        """
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                'View is not defined, pass it as a context variable'
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError('Define adapter_class in view')

        adapter = adapter_class()
        app = adapter.get_provider().get_app(request)

        if('access_token' in attrs) and ('token_secret' in attrs):
            access_token = attrs.get('access_token')
            token_secret = attrs.get('token_secret')
        else:
            raise serializers.ValidationError('Incorrect input. access_token and token_secret are required.')

        request.session['oauth_api.twitter.com_access_token'] = {
            'oauth_token': access_token,
            'oauth_token_secret': token_secret,
        }
        token = SocialToken(token=access_token, token_secret=token_secret)
        token.app = app

        try:
            login = self.get_social_login(adapter, app, token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError('Incorrect value')

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)
        attrs['user'] = login.account.user

        return attrs
