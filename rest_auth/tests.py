import json
import os
import sys
from datetime import datetime, date, time

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.client import Client, MULTIPART_CONTENT
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from registration.models import RegistrationProfile
from rest_framework.serializers import _resolve_model


class APIClient(Client):

    def patch(self, path, data='', content_type=MULTIPART_CONTENT, follow=False, **extra):
        return self.generic('PATCH', path, data, content_type, **extra)

    def options(self, path, data='', content_type=MULTIPART_CONTENT, follow=False, **extra):
        return self.generic('OPTIONS', path, data, content_type, **extra)


class CustomJSONEncoder(json.JSONEncoder):
    """
    Convert datetime/date objects into isoformat
    """

    def default(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        else:
            return super(CustomJSONEncoder, self).default(obj)


class BaseAPITestCase(object):

    """
    base for API tests:
        * easy request calls, f.e.: self.post(url, data), self.get(url)
        * easy status check, f.e.: self.post(url, data, status_code=200)
    """
    def send_request(self, request_method, *args, **kwargs):
        request_func = getattr(self.client, request_method)
        status_code = None
        if not 'content_type' in kwargs and request_method != 'get':
            kwargs['content_type'] = 'application/json'
        if 'data' in kwargs and request_method != 'get' and kwargs['content_type'] == 'application/json':
            data = kwargs.get('data', '')
            kwargs['data'] = json.dumps(data, cls=CustomJSONEncoder)
        if 'status_code' in kwargs:
            status_code = kwargs.pop('status_code')

        # check_headers = kwargs.pop('check_headers', True)
        if hasattr(self, 'token'):
            kwargs['HTTP_AUTHORIZATION'] = 'Token %s' % self.token

        if hasattr(self, 'company_token'):
            kwargs[
                'HTTP_AUTHORIZATION'] = 'Company-Token %s' % self.company_token

        self.response = request_func(*args, **kwargs)
        is_json = bool(
            filter(lambda x: 'json' in x, self.response._headers['content-type']))
        if is_json and self.response.content:
            self.response.json = json.loads(self.response.content)
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

    def put(self, *args, **kwargs):
        return self.send_request('put', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.send_request('delete', *args, **kwargs)

    def options(self, *args, **kwargs):
        return self.send_request('options', *args, **kwargs)

    def post_file(self, *args, **kwargs):
        kwargs['content_type'] = MULTIPART_CONTENT
        return self.send_request('post', *args, **kwargs)

    def get_file(self, *args, **kwargs):
        content_type = None
        if 'content_type' in kwargs:
            content_type = kwargs.pop('content_type')
        response = self.send_request('get', *args, **kwargs)
        if content_type:
            self.assertEqual(
                bool(filter(lambda x: content_type in x, response._headers['content-type'])), True)
        return response

    def init(self):
        settings.DEBUG = True
        self.client = APIClient()


# -----------------------
#  T E S T   H E R E
# -----------------------

user_profile_model = _resolve_model(
    getattr(settings, 'REST_PROFILE_MODULE', None))

class LoginAPITestCase(TestCase, BaseAPITestCase):

    """
    just run: python manage.py test rest_auth
    """

    USERNAME = 'person'
    PASS = 'person'


    def setUp(self):
        self.init()
        self.login_url = reverse('rest_login')
        self.password_change_url = reverse('rest_password_change')
        self.register_url = reverse('rest_register')

    def test_login(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        # there is no users in db so it should throw error (401)
        self.post(self.login_url, data=payload, status_code=401)

        self.post(self.password_change_url, status_code=403)

        # create user
        user = User.objects.create_user(self.USERNAME, '', self.PASS)

        self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual('key' in self.response.json.keys(), True)
        self.token = self.response.json['key']

        self.post(self.password_change_url, status_code=400)

        # test inactive user
        user.is_active = False
        user.save()
        self.post(self.login_url, data=payload, status_code=401)

        # test wrong username/password
        payload = {
            "username": self.USERNAME+'?',
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=401)

        # test empty payload
        self.post(self.login_url, data={}, status_code=400)


    def test_password_change(self):
        login_payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        user = User.objects.create_user(self.USERNAME, '', self.PASS)
        self.post(self.login_url, data=login_payload, status_code=200)
        self.token = self.response.json['key']

        new_password_payload = {
            "new_password1": "new_person",
            "new_password2": "new_person"
        }
        self.post(self.password_change_url, data=new_password_payload,
            status_code=200)

        # user should not be able to login using old password
        self.post(self.login_url, data=login_payload, status_code=401)

        # new password should work
        login_payload['password'] = new_password_payload['new_password1']
        self.post(self.login_url, data=login_payload, status_code=200)

        # pass1 and pass2 are not equal
        new_password_payload = {
            "new_password1": "new_person1",
            "new_password2": "new_person"
        }
        self.post(self.password_change_url, data=new_password_payload,
            status_code=400)

        # send empty payload
        self.post(self.password_change_url, data={}, status_code=400)

    def test_registration_user_with_profile(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS,
            "email": "person@world.com",
            "newsletter_subscribe": "false"
        }

        # test empty payload
        self.post(self.register_url, data={}, status_code=400)

        self.post(self.register_url, data=payload, status_code=201)

        activation_key = RegistrationProfile.objects.latest('id').activation_key
        verify_url = reverse('verify_email',
            kwargs={'activation_key': activation_key})

        # new user at this point shouldn't be active
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.is_active, False)

        # let's active new user and check is_active flag
        self.get(verify_url)
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.is_active, True)
        #user_profile = user_profile_model.objects.get(user=new_user)
        #self.assertIsNotNone(user_profile)

    def test_registration_user_without_profile(self):

        payload = {
            "username": self.USERNAME,
            "password": self.PASS,
            "email": "person1@world.com"
        }

        self.post(self.register_url, data=payload, status_code=201)

        activation_key = RegistrationProfile.objects.latest('id').activation_key
        verify_url = reverse('verify_email',
            kwargs={'activation_key': activation_key})

        # new user at this point shouldn't be active
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.is_active, False)

        # let's active new user and check is_active flag
        self.get(verify_url)
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.is_active, True)

        # user_profile = user_profile_model.objects.get(user=new_user)
        # self.assertIsNotNone(user_profile)
