from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.provider import GRAPH_API_URL
import responses

from rest_framework import status

from .test_base import BaseAPITestCase


class TestSocialAuth(TestCase, BaseAPITestCase):

    urls = 'tests.urls'

    USERNAME = 'person'
    PASS = 'person'
    EMAIL = "person1@world.com"
    REGISTRATION_DATA = {
        "username": USERNAME,
        "password1": PASS,
        "password2": PASS,
        "email": EMAIL
    }

    def setUp(self):
        self.init()

        social_app = SocialApp.objects.create(
            provider='facebook',
            name='Facebook',
            client_id='123123123',
            secret='321321321',
        )
        site = Site.objects.get_current()
        social_app.sites.add(site)
        self.graph_api_url = GRAPH_API_URL + '/me'

    @responses.activate
    def test_failed_social_auth(self):
        # fake response
        responses.add(
            responses.GET,
            self.graph_api_url,
            body='',
            status=400,
            content_type='application/json'
        )

        payload = {
            'access_token': 'abc123'
        }
        self.post(self.fb_login_url, data=payload, status_code=400)

    @responses.activate
    def test_social_auth(self):
        # fake response for facebook call
        resp_body = '{"id":"123123123123","first_name":"John","gender":"male","last_name":"Smith","link":"https:\\/\\/www.facebook.com\\/john.smith","locale":"en_US","name":"John Smith","timezone":2,"updated_time":"2014-08-13T10:14:38+0000","username":"john.smith","verified":true}'  # noqa
        responses.add(
            responses.GET,
            self.graph_api_url,
            body=resp_body,
            status=200,
            content_type='application/json'
        )

        users_count = get_user_model().objects.all().count()
        payload = {
            'access_token': 'abc123'
        }

        self.post(self.fb_login_url, data=payload, status_code=200)
        self.assertIn('key', self.response.json.keys())
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

        # make sure that second request will not create a new user
        self.post(self.fb_login_url, data=payload, status_code=200)
        self.assertIn('key', self.response.json.keys())
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

    @responses.activate
    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION='mandatory',
        ACCOUNT_EMAIL_REQUIRED=True,
        REST_SESSION_LOGIN=False
    )
    def test_edge_case(self):
        resp_body = '{"id":"123123123123","first_name":"John","gender":"male","last_name":"Smith","link":"https:\\/\\/www.facebook.com\\/john.smith","locale":"en_US","name":"John Smith","timezone":2,"updated_time":"2014-08-13T10:14:38+0000","username":"john.smith","verified":true,"email":"%s"}'  # noqa
        responses.add(
            responses.GET,
            self.graph_api_url,
            body=resp_body % self.EMAIL,
            status=200,
            content_type='application/json'
        )

        # test empty payload
        self.post(self.register_url, data={}, status_code=400)
        self.post(
            self.register_url,
            data=self.REGISTRATION_DATA,
            status_code=201
        )
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.username, self.REGISTRATION_DATA['username'])

        # verify email
        email_confirmation = new_user.emailaddress_set.get(email=self.EMAIL)\
            .emailconfirmation_set.order_by('-created')[0]
        self.post(
            self.veirfy_email_url,
            data={"key": email_confirmation.key},
            status_code=status.HTTP_200_OK
        )

        self._login()
        self._logout()

        payload = {
            'access_token': 'abc123'
        }

        self.post(self.fb_login_url, data=payload, status_code=200)
        self.assertIn('key', self.response.json.keys())
