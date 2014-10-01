from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import serializers
from rest_framework.serializers import _resolve_model
from rest_framework.authtoken.models import Token


profile_model_path = lambda: getattr(settings, 'REST_PROFILE_MODULE', None)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)


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
        fields = ('username', 'email', 'first_name', 'last_name')


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    """
    ModelSerializer that allows fields argument to control fields
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserUpdateSerializer(DynamicFieldsModelSerializer):

    """
    User model w/o username and password
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name')



def get_user_registration_profile_serializer(*args, **kwargs):
    if profile_model_path():
        class UserRegistrationProfileSerializer(serializers.ModelSerializer):

            """
            Serializer that includes all profile fields except for user fk / id.
            """
            class Meta:

                model = _resolve_model(profile_model_path())
                fields = filter(lambda x: x != 'id' and x != 'user',
                                map(lambda x: x.name, model._meta.fields))
    else:
        class UserRegistrationProfileSerializer(serializers.Serializer):
            pass
    return UserRegistrationProfileSerializer


def get_user_profile_serializer(*args, **kwargs):
    if profile_model_path():
        class UserProfileSerializer(serializers.ModelSerializer):

            """
            Serializer for UserProfile model.
            """

            user = UserDetailsSerializer()

            class Meta:
                # http://stackoverflow.com/questions/4881607/django-get-model-from-string
                model = _resolve_model(profile_model_path())

            def __init__(self, *args, **kwargs):
                super(UserProfileSerializer, self).__init__(*args, **kwargs)
    else:
        class UserProfileSerializer(serializers.Serializer):
            pass
    return UserProfileSerializer


def get_user_profile_update_serializer(*args, **kwargs):
    if profile_model_path():
        class UserProfileUpdateSerializer(serializers.ModelSerializer):

            """
            Serializer for updating User and UserProfile model.
            """

            user = UserUpdateSerializer()

            class Meta:
                # http://stackoverflow.com/questions/4881607/django-get-model-from-string
                model = _resolve_model(profile_model_path())
    else:
        class UserProfileUpdateSerializer(serializers.Serializer):
            pass
    return UserProfileUpdateSerializer


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
