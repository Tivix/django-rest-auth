from axes.helpers import get_lockout_message
from rest_auth import serializers
from rest_auth.serializers import LoginSerializer
from rest_framework import exceptions


# noinspection PyAbstractClass
class RestAuthAxesLoginSerializer(LoginSerializer):

    def validate(self, attrs) -> dict:
        try:
            return super().validate(attrs)
        except exceptions.ValidationError as e:
            if getattr(self.context['request'], 'axes_locked_out', None):
                raise serializers.ValidationError(get_lockout_message())
            raise e
