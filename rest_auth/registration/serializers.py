from django.http import HttpRequest
from rest_framework import serializers
from requests.exceptions import HTTPError
from allauth.socialaccount.helpers import complete_social_login


class SocialLoginSerializer(serializers.Serializer):

    access_token = serializers.CharField(required=True)

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        view = self.context.get('view')
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request

        if not view:
            raise serializers.ValidationError(
                'View is not defined, pass it as a context variable'
            )

        self.adapter_class = getattr(view, 'adapter_class', None)

        if not self.adapter_class:
            raise serializers.ValidationError('Define adapter_class in view')

        self.adapter = self.adapter_class()
        app = self.adapter.get_provider().get_app(request)
        token = self.adapter.parse_token({'access_token': access_token})
        token.app = app

        try:
            login = self.adapter.complete_login(request, app, token,
                                                response=access_token)

            login.token = token
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError('Incorrect value')

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)
        attrs['user'] = login.account.user

        return attrs
