from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for Django User model and most of its fields.
    """

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class VerifyEmailSerializer(serializers.Serializer):
    pass
