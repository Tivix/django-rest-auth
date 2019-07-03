from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from myapp import serializers


class TestRestAuthAxesLoginSerializer(TestCase):

    def setUp(self) -> None:
        self.request = HttpRequest()

    def test_validate_wrong_user(self) -> None:
        serializer = serializers.RestAuthAxesLoginSerializer(
            context=dict(request=self.request)
        )
        with self.assertRaisesMessage(ValidationError, 'Unable to log in with provided credentials.'):
            serializer.validate({
                'username': 'test',
                'email': 'test@example.com',
                'password': 'test'
            })

    def test_validate_good_user(self) -> None:
        User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test'
        )
        serializer = serializers.RestAuthAxesLoginSerializer(
            context=dict(request=self.request)
        )
        attrs = serializer.validate({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'test'
        })

        self.assertIsNotNone(attrs)

    def test_validate_axes_locked_out(self) -> None:
        good_password_creds = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'good_password'
        }

        bad_password_creds = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'bad_password'
        }

        User.objects.create_user(**good_password_creds)
        serializer = serializers.RestAuthAxesLoginSerializer(
            context=dict(request=self.request)
        )

        for i in range(settings.AXES_FAILURE_LIMIT - 1):
            with self.assertRaisesMessage(ValidationError, 'Unable to log in with provided credentials.'):
                serializer.validate(bad_password_creds)

        account_locked_message = 'Account locked: too many login attempts. Contact an admin to unlock your account.'

        with self.assertRaisesMessage(ValidationError, account_locked_message):
            serializer.validate(bad_password_creds)

        with self.assertRaisesMessage(ValidationError, account_locked_message):
            serializer.validate(good_password_creds)
