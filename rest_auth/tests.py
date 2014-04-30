import json
import os
from datetime import datetime, date, time
from pprint import pprint

from django.conf import settings
from django.test.client import Client, MULTIPART_CONTENT
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


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

    img = os.path.join(settings.STATICFILES_DIRS[0][1], 'images/no_profile_photo.png')

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
            kwargs['HTTP_AUTHORIZATION'] = 'Company-Token %s' % self.company_token

        self.response = request_func(*args, **kwargs)
        is_json = bool(filter(lambda x: 'json' in x, self.response._headers['content-type']))
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
            self.assertEqual(bool(filter(lambda x: content_type in x, response._headers['content-type'])), True)
        return response

    def init(self):
        settings.DEBUG = True
        self.client = APIClient()



# -----------------------
#  T E S T   H E R E
# -----------------------

class LoginAPITestCase(TestCase, BaseAPITestCase):
    """
    just run: python manage.py test rest_auth
    """

    USERNAME = 'person'
    PASS = 'person'

    def setUp(self):
        self.init()
        self.login_url = reverse('rest_login')

    def test_login(self):
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        # there is no users in db so it should throw error (401)
        self.post(self.login_url, data=payload, status_code=401)

        # you can easily print response
        pprint(self.response.json)

        # create user
        user = User.objects.create_user(self.USERNAME, '', self.PASS)

        self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual('key' in self.response.json.keys(), True)


        self.token = self.response.json['key']
        # TODO:
        # now all urls that required token should be available
        # would be perfect to test one of


        # TODO:
        # another case to test - make user inactive and test if login is impossible
