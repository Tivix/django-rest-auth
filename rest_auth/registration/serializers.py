from django.http import HttpRequest
from rest_framework import serializers
from requests.exceptions import HTTPError
from allauth.socialaccount.helpers import complete_social_login


class SocialLoginSerializer(serializers.Serializer):

    access_token = serializers.CharField(required=False)
    code = serializers.CharField(required=False)

    def validate(self, attrs):

        view = self.context.get('view')
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request

        if not view:
            raise serializers.ValidationError(
                'View is not defined, pass it ' +
                'as a context variable'
            )
        self.adapter_class = getattr(view, 'adapter_class', None)

        if not self.adapter_class:
            raise serializers.ValidationError('Define adapter_class in view')

        self.adapter = self.adapter_class()
        app = self.adapter.get_provider().get_app(request)

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token
        # We have the access_token straight
        if('access_token' in attrs):
            access_token = attrs.get('access_token')
        # We did not get the access_token, but authorization code instead
        elif('code' in attrs):
            self.callback_url = getattr(view, 'callback_url', None)

            if not self.callback_url:
                raise serializers.ValidationError(
                    'Define callback_url in view'
                )

            code = attrs.get('code')

            provider = self.adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.adapter_class(
                request,
                app.client_id,
                app.secret,
                self.adapter.access_token_method,
                self.adapter.access_token_url,
                self.callback_url,
                scope
            )
            token = client.get_access_token(code)
            access_token = token['access_token']

        token = self.adapter.parse_token({'access_token': access_token})
        token.app = app

        try:
            login = self.adapter.complete_login(request, app, token,
                                                response=access_token)
            token.account = login.account
            login.token = token
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError('Incorrect value')

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)
        attrs['user'] = login.account.user

        return attrs
