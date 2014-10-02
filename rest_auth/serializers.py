from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


class LoginSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        attrs = super(LoginSerializer, self).validate(attrs)

        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                user = attrs['user']
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError('E-mail is not verified.')
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key',)


class UserDetailsSerializer(serializers.ModelSerializer):

    """
    User model w/o password
    """
    class Meta:
        model = get_user_model()
        exclude = ('password', 'groups', 'user_permissions', 'is_staff',
            'is_superuser')
        read_only_fields = ('id', 'last_login', 'is_active', 'date_joined')


class SetPasswordSerializer(serializers.Serializer):

    """
    Serializer for changing Django User password.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        return super(SetPasswordSerializer, self).__init__(*args, **kwargs)


class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()
