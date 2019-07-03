from axes.helpers import get_lockout_message
from rest_auth import serializers
from rest_auth.serializers import LoginSerializer
from rest_framework import exceptions


# noinspection PyAbstractClass
class RestAuthLoginSerializer(LoginSerializer):

    def validate(self, attrs):
        try:
            attrs = super().validate(attrs)
        except exceptions.ValidationError:
            if getattr(self.context['request'], 'axes_locked_out', None):
                raise serializers.ValidationError(get_lockout_message())
        return attrs
