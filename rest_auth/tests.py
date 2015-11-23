import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.client import Client, MULTIPART_CONTENT
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.test.utils import override_settings
from django.contrib.sites.models import Site
from django.utils.encoding import force_text

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.provider import GRAPH_API_URL
import responses

from rest_framework import status


class APIClient(Client):

    def patch(self, path, data='', content_type=MULTIPART_CONTENT, follow=False, **extra):
        return self.generic('PATCH', path, data, content_type, **extra)

    def options(self, path, data='', content_type=MULTIPART_CONTENT, follow=False, **extra):
        return self.generic('OPTIONS', path, data, content_type, **extra)


class BaseAPITestCase(object):

    """
    base for API tests:
        * easy request calls, f.e.: self.post(url, data), self.get(url)
        * easy status check, f.e.: self.post(url, data, status_code=200)
    """
    def send_request(self, request_method, *args, **kwargs):
        request_func = getattr(self.client, request_method)
        status_code = None
        if 'content_type' not in kwargs and request_method != 'get':
            kwargs['content_type'] = 'application/json'
        if 'data' in kwargs and request_method != 'get' and kwargs['content_type'] == 'application/json':
            data = kwargs.get('data', '')
            kwargs['data'] = json.dumps(data)  # , cls=CustomJSONEncoder
        if 'status_code' in kwargs:
            status_code = kwargs.pop('status_code')

        # check_headers = kwargs.pop('check_headers', True)
        if hasattr(self, 'token'):
            kwargs['HTTP_AUTHORIZATION'] = 'Token %s' % self.token

        self.response = request_func(*args, **kwargs)
        is_json = bool(
            [x for x in self.response._headers['content-type'] if 'json' in x])
        if is_json and self.response.content:
            self.response.json = json.loads(force_text(self.response.content))
        else:
            self.response.json = {}
        if status_code:
            self.assertEqual(self.response.status_code, status_code)
        return self.response

    def post(self, *args, **kwargs):
        return self.send_request('post', *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.send_request('get', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.send_request('patch', *args, **kwargs)

    # def put(self, *args, **kwargs):
    #     return self.send_request('put', *args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     return self.send_request('delete', *args, **kwargs)

    # def options(self, *args, **kwargs):
    #     return self.send_request('options', *args, **kwargs)

    # def post_file(self, *args, **kwargs):
    #     kwargs['content_type'] = MULTIPART_CONTENT
    #     return self.send_request('post', *args, **kwargs)

    # def get_file(self, *args, **kwargs):
    #     content_type = None
    #     if 'content_type' in kwargs:
    #         content_type = kwargs.pop('content_type')
    #     response = self.send_request('get', *args, **kwargs)
    #     if content_type:
    #         self.assertEqual(
    #             bool(filter(lambda x: content_type in x, response._headers['content-type'])), True)
    #     return response

    def init(self):
        settings.DEBUG = True
        self.client = APIClient()

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.password_change_url = reverse('rest_password_change')
        self.register_url = reverse('rest_register')
        self.password_reset_url = reverse('rest_password_reset')
        self.user_url = reverse('rest_user_details')
        self.veirfy_email_url = reverse('rest_verify_email')
        self.fb_login_url = reverse('fb_login')

    def _login(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=status.HTTP_200_OK)

    def _logout(self):
        self.post(self.logout_url, status=status.HTTP_200_OK)


# -----------------------
#  T E S T   H E R E
# -----------------------


class APITestCase1(TestCase, BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    urls = 'rest_auth.test_urls'

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

    def test_login(self):
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

    def test_password_change(self):
        login_payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        get_user_model().objects.create_user(self.USERNAME, '', self.PASS)
        self.post(self.login_url, data=login_payload, status_code=200)
        self.token = self.response.json['key']

        new_password_payload = {
            "new_password1": "new_person",
            "new_password2": "new_person"
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=200
        )

        # user should not be able to login using old password
        self.post(self.login_url, data=login_payload, status_code=400)

        # new password should work
        login_payload['password'] = new_password_payload['new_password1']
        self.post(self.login_url, data=login_payload, status_code=200)

        # pass1 and pass2 are not equal
        new_password_payload = {
            "new_password1": "new_person1",
            "new_password2": "new_person"
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=400
        )

        # send empty payload
        self.post(self.password_change_url, data={}, status_code=400)

    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_password_change_with_old_password(self):
        login_payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        get_user_model().objects.create_user(self.USERNAME, '', self.PASS)
        self.post(self.login_url, data=login_payload, status_code=200)
        self.token = self.response.json['key']

        new_password_payload = {
            "old_password": "%s!" % self.PASS,  # wrong password
            "new_password1": "new_person",
            "new_password2": "new_person"
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=400
        )

        new_password_payload = {
            "old_password": self.PASS,
            "new_password1": "new_person",
            "new_password2": "new_person"
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=200
        )

        # user should not be able to login using old password
        self.post(self.login_url, data=login_payload, status_code=400)

        # new password should work
        login_payload['password'] = new_password_payload['new_password1']
        self.post(self.login_url, data=login_payload, status_code=200)

    def test_password_reset(self):
        user = get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)

        # call password reset
        mail_count = len(mail.outbox)
        payload = {'email': self.EMAIL}
        self.post(self.password_reset_url, data=payload, status_code=200)
        self.assertEqual(len(mail.outbox), mail_count + 1)

        url_kwargs = self._generate_uid_and_token(user)
        url = reverse('rest_password_reset_confirm')

        # wrong token
        data = {
            'new_password1': self.NEW_PASS,
            'new_password2': self.NEW_PASS,
            'uid': force_text(url_kwargs['uid']),
            'token': '-wrong-token-'
        }
        self.post(url, data=data, status_code=400)

        # wrong uid
        data = {
            'new_password1': self.NEW_PASS,
            'new_password2': self.NEW_PASS,
            'uid': '-wrong-uid-',
            'token': url_kwargs['token']
        }
        self.post(url, data=data, status_code=400)

        # wrong token and uid
        data = {
            'new_password1': self.NEW_PASS,
            'new_password2': self.NEW_PASS,
            'uid': '-wrong-uid-',
            'token': '-wrong-token-'
        }
        self.post(url, data=data, status_code=400)

        # valid payload
        data = {
            'new_password1': self.NEW_PASS,
            'new_password2': self.NEW_PASS,
            'uid': force_text(url_kwargs['uid']),
            'token': url_kwargs['token']
        }
        url = reverse('rest_password_reset_confirm')
        self.post(url, data=data, status_code=200)

        payload = {
            "username": self.USERNAME,
            "password": self.NEW_PASS
        }
        self.post(self.login_url, data=payload, status_code=200)

    def test_password_reset_with_invalid_email(self):
        get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)

        # call password reset
        mail_count = len(mail.outbox)
        payload = {'email': 'nonexisting@email.com'}
        self.post(self.password_reset_url, data=payload, status_code=400)
        self.assertEqual(len(mail.outbox), mail_count)

    def test_user_details(self):
        user = get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=200)
        self.token = self.response.json['key']
        self.get(self.user_url, status_code=200)

        self.patch(self.user_url, data=self.BASIC_USER_DATA, status_code=200)
        user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(user.first_name, self.response.json['first_name'])
        self.assertEqual(user.last_name, self.response.json['last_name'])
        self.assertEqual(user.email, self.response.json['email'])

    def test_registration(self):
        user_count = get_user_model().objects.all().count()

        # test empty payload
        self.post(self.register_url, data={}, status_code=400)

        self.post(self.register_url, data=self.REGISTRATION_DATA, status_code=201)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.username, self.REGISTRATION_DATA['username'])

        self._login()
        self._logout()

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION='mandatory',
        ACCOUNT_EMAIL_REQUIRED=True
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

        self.post(
            self.register_url,
            data=self.REGISTRATION_DATA_WITH_EMAIL,
            status_code=status.HTTP_201_CREATED
        )
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
            self.veirfy_email_url,
            data={"key": email_confirmation.key},
            status_code=status.HTTP_200_OK
        )

        # try to login again
        self._login()
        self._logout()


class TestSocialAuth(TestCase, BaseAPITestCase):

    urls = 'rest_auth.test_urls'

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
