from allauth.account import app_settings as account_app_settings
from dj_rest_auth.registration.app_settings import register_permission_classes
from dj_rest_auth.registration.views import RegisterView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.test import APIRequestFactory

from .mixins import CustomPermissionClass, TestsMixin

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


@override_settings(ROOT_URLCONF="tests.urls")
class APIBasicTests(TestsMixin, TestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    # urls = 'tests.urls'

    USERNAME = 'person'
    PASS = 'person'
    EMAIL = "person1@world.com"
    NEW_PASS = 'new-test-pass'
    REGISTRATION_VIEW = 'rest_auth.runtests.RegistrationView'

    # data without user profile
    REGISTRATION_DATA = {
        "username": USERNAME,
        "password1": PASS,
        "password2": PASS
    }

    REGISTRATION_DATA_WITH_EMAIL = REGISTRATION_DATA.copy()
    REGISTRATION_DATA_WITH_EMAIL['email'] = EMAIL

    BASIC_USER_DATA = {
        'first_name': "John",
        'last_name': 'Smith',
        'email': EMAIL
    }
    USER_DATA = BASIC_USER_DATA.copy()
    USER_DATA['newsletter_subscribe'] = True

    def setUp(self):
        self.init()

    def _generate_uid_and_token(self, user):
        result = {}
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode

        result['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        result['token'] = default_token_generator.make_token(user)
        return result

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.EMAIL)
    def test_login_failed_email_validation(self):
        payload = {
            "email": '',
            "password": self.PASS
        }

        resp = self.post(self.login_url, data=payload, status_code=400)
        self.assertEqual(resp.json['non_field_errors'][0], u'Must include "email" and "password".')

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.USERNAME)
    def test_login_failed_username_validation(self):
        payload = {
            "username": '',
            "password": self.PASS
        }

        resp = self.post(self.login_url, data=payload, status_code=400)
        self.assertEqual(resp.json['non_field_errors'][0], u'Must include "username" and "password".')

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_login_failed_username_email_validation(self):
        payload = {
            "password": self.PASS
        }

        resp = self.post(self.login_url, data=payload, status_code=400)
        self.assertEqual(resp.json['non_field_errors'][0], u'Must include either "username" or "email" and "password".')

    def test_allauth_login_with_username(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        # there is no users in db so it should throw error (400)
        self.post(self.login_url, data=payload, status_code=400)

        self.post(self.password_change_url, status_code=403)

        # create user
        user = get_user_model().objects.create_user(self.USERNAME, '', self.PASS)

        self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual('key' in self.response.json.keys(), True)
        self.token = self.response.json['key']

        self.post(self.password_change_url, status_code=400)

        # test inactive user
        user.is_active = False
        user.save()
        self.post(self.login_url, data=payload, status_code=400)

        # test wrong username/password
        payload = {
            "username": self.USERNAME + '?',
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=400)

        # test empty payload
        self.post(self.login_url, data={}, status_code=400)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.EMAIL)
    def test_allauth_login_with_email(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS
        }
        # there is no users in db so it should throw error (400)
        self.post(self.login_url, data=payload, status_code=400)

        self.post(self.password_change_url, status_code=403)

        # create user
        get_user_model().objects.create_user(self.EMAIL, email=self.EMAIL, password=self.PASS)

        self.post(self.login_url, data=payload, status_code=200)

    @override_settings(REST_USE_JWT=True)
    @override_settings(JWT_AUTH_COOKIE='jwt-auth')
    def test_login_jwt_sets_cookie(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        get_user_model().objects.create_user(self.USERNAME, '', self.PASS)
        resp = self.post(self.login_url, data=payload, status_code=200)
        self.assertTrue('jwt-auth' in resp.cookies.keys())

    @override_settings(REST_USE_JWT=True)
    @override_settings(JWT_AUTH_COOKIE='jwt-auth')
    def test_logout_jwt_deletes_cookie(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        get_user_model().objects.create_user(self.USERNAME, '', self.PASS)
        self.post(self.login_url, data=payload, status_code=200)
        resp = self.post(self.logout_url, status=200)
        self.assertEqual('', resp.cookies.get('jwt-auth').value)

    @override_settings(REST_USE_JWT=True)
    @override_settings(JWT_AUTH_COOKIE='jwt-auth')
    @override_settings(REST_FRAMEWORK=dict(
        DEFAULT_AUTHENTICATION_CLASSES=[
            'dj_rest_auth.utils.JWTCookieAuthentication'
        ]
    ))
    @override_settings(REST_SESSION_LOGIN=False)
    def test_cookie_authentication(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        get_user_model().objects.create_user(self.USERNAME, '', self.PASS)
        resp = self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual(['jwt-auth'], list(resp.cookies.keys()))
        resp = self.get('/protected-view/')
        self.assertEquals(resp.status_code, 200)

    def test_registration_with_invalid_password(self):
        data = self.REGISTRATION_DATA.copy()
        data['password2'] = 'foobar'

        self.post(self.register_url, data=data, status_code=400)

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION='mandatory',
        ACCOUNT_EMAIL_REQUIRED=True,
        ACCOUNT_EMAIL_CONFIRMATION_HMAC=False
    )
    def test_registration_with_email_verification(self):
        user_count = get_user_model().objects.all().count()
        mail_count = len(mail.outbox)

        # test empty payload
        self.post(
            self.register_url,
            data={},
            status_code=status.HTTP_400_BAD_REQUEST
        )

        result = self.post(
            self.register_url,
            data=self.REGISTRATION_DATA_WITH_EMAIL,
            status_code=status.HTTP_201_CREATED
        )
        self.assertNotIn('key', result.data)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)
        self.assertEqual(len(mail.outbox), mail_count + 1)
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.username, self.REGISTRATION_DATA['username'])

        # email is not verified yet
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        self.post(
            self.login_url,
            data=payload,
            status=status.HTTP_400_BAD_REQUEST
        )

        # verify email
        email_confirmation = new_user.emailaddress_set.get(email=self.EMAIL)\
            .emailconfirmation_set.order_by('-created')[0]
        self.post(
            self.verify_email_url,
            data={"key": email_confirmation.key},
            status_code=status.HTTP_200_OK
        )

        # try to login again
        self._login()
        self._logout()

    @override_settings(ACCOUNT_LOGOUT_ON_GET=True)
    def test_logout_on_get(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }

        # create user
        get_user_model().objects.create_user(self.USERNAME, '', self.PASS)

        self.post(self.login_url, data=payload, status_code=200)
        self.get(self.logout_url, status=status.HTTP_200_OK)

    @override_settings(ACCOUNT_LOGOUT_ON_GET=False)
    def test_logout_on_post_only(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }

        # create user
        get_user_model().objects.create_user(self.USERNAME, '', self.PASS)

        self.post(self.login_url, data=payload, status_code=status.HTTP_200_OK)
        self.get(self.logout_url, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
