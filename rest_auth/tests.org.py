import requests
import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings

from rest_framework.serializers import _resolve_model

from registration.models import RegistrationProfile


# Get the UserProfile model from the setting value
user_profile_model = _resolve_model(getattr(settings, 'REST_PROFILE_MODULE', None))

# Get the REST Registration Backend for django-registration
registration_backend = getattr(settings, 'REST_REGISTRATION_BACKEND', 'rest_auth.backends.rest_registration.RESTRegistrationView')


class RegistrationAndActivationTestCase(TestCase):
    """
    Unit Test for registering and activating a new user

    This test case assumes that the local server runs at port 8000.
    """

    def setUp(self):
        self.url = "http://localhost:8000/rest_auth/register/"
        self.headers = {"content-type": "application/json"}

    def test_successful_registration(self):
        print 'Registering a new user'
        payload = {"username": "person", "password": "person", "email": "person@world.com", "newsletter_subscribe": "false"}

        print 'The request will attempt to register:'
        print 'Django User object'
        print 'Username: %s\nPassword: %s\nEmail: %s\n' % ('person', 'person', 'person@world.com')
        print 'Django UserProfile object'
        print 'newsletter_subscribe: false'
        print 'Sending a POST request to register API'

        r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 201):
            print r.content

            print 'Activating a new user'

            # Get the latest activation key from RegistrationProfile model
            activation_key = RegistrationProfile.objects.latest('id').activation_key

            # Set the url and GET the request to verify and activate a new user
            url = "http://localhost:8000/rest_auth/verify-email/" + activation_key + "/"
            r = requests.get(url)

            print "Sending a GET request to activate the user from verify-email API"

            if self.assertEqual(r.status_code, 200):
                print r.content

                # Get the latest User object
                new_user = get_user_model().objects.latest('id')
                print "Got the new user %s" % new_user.username

                try:
                    print "Got the new user profile %s" % (user_profile_model.objects.get(user=new_user))
                except user_profile_model.DoesNotExist:
                    pass

    def test_successful_registration_without_userprofile_model(self):
        print 'Registering a new user'
        payload = {"username": "person1", "password": "person1", "email": "person1@world.com"}

        print 'The request will attempt to register:'
        print 'Django User object'
        print 'Username: %s\nPassword: %s\nEmail: %s\n' % ('person1', 'person1', 'person1@world.com')
        print 'No Django UserProfile object'
        print 'Sending a POST request to register API'

        r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 201):
            print r.content

            print 'Activating a new user'

            # Get the latest activation key from RegistrationProfile model
            activation_key = RegistrationProfile.objects.latest('id').activation_key

            # Set the url and GET the request to verify and activate a new user
            url = "http://localhost:8000/rest_auth/verify-email/" + activation_key + "/"
            r = requests.get(url)

            print "Sending a GET request to activate the user from verify-email API"

            if self.assertEqual(r.status_code, 200):
                print r.content

                # Get the latest User object
                new_user = get_user_model().objects.latest('id')
                print "Got the new user %s" % new_user.username

                try:
                    print "Got the new user profile %s" % (user_profile_model.objects.get(user=new_user))
                except user_profile_model.DoesNotExist:
                    pass

    def test_required_fields_for_registration(self):
        print 'Registering a new user'
        payload = {}

        print 'The request will attempt to register with no data provided.'
        print 'Sending a POST request to register API'

        r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 400):
            print r.content


class LoginTestCase(TestCase):
    """
    Unit Test for logging in

    This test case assumes that the local server runs at port 8000.
    """

    def setUp(self):
        self.url = "http://localhost:8000/rest_auth/login/"
        self.headers = {"content-type": "application/json"}

    def test_successful_login(self):
        print 'Logging in as a new user'
        payload = {"username": "person", "password": "person"}

        print 'The request will attempt to login:'
        print 'Username: %s\nPassword: %s' % ('person', 'person')
        print 'Sending a POST request to login API'

        r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 200):
            print r.content

            print "Got the REST Token: " + r.json()['key']

    def test_invalid_login(self):
        print 'Logging in as a new user'
        payload = {"username": "person", "password": "person32"}

        print 'The request will attempt to login:'
        print 'Username: %s\nPassword: %s' % ('person', 'person32')
        print 'Sending a POST request to login API'

        r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 401):
            print r.content

    def test_required_fields_for_login(self):
        print 'Logging in as a new user'
        payload = {}

        print 'The request will attempt to login with no data provided.'
        print 'Sending a POST request to login API'

        r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 400):
            print r.content


class PasswordChangeCase(TestCase):
    """
    Unit Test for changing the password while logged in

    This test case assumes that the local server runs at port 8000.
    """

    def setUp(self):
        self.url = "http://localhost:8000/rest_auth/password/change/"
        self.headers = {"content-type": "application/json"}

    def test_successful_password_change(self):
        print 'Logging in'
        payload = {"username": "person", "password": "person"}
        login_url = "http://localhost:8000/rest_auth/login/"

        print 'Sending a POST request to login API'

        r = requests.post(login_url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 200):
            print r.content

            print "Got the REST Token: " + r.json()['key']

            self.token = r.json()['key']
            self.headers['authorization'] = "Token " + r.json()['key']

            payload = {"new_password1": "new_person", "new_password2": "new_person"}
            print 'Sending a POST request to password change API'

            r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

            if self.assertEqual(r.status_code, 200):
                print r.content

                payload = {"new_password1": "person", "new_password2": "person"}
                print 'Sending a POST request to password change API'

                r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

                if self.assertEqual(r.status_code, 200):
                    print r.content

    def test_invalid_password_change(self):
        print 'Logging in'
        payload = {"username": "person", "password": "person"}
        login_url = "http://localhost:8000/rest_auth/login/"

        print 'Sending a POST request to login API'

        r = requests.post(login_url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 200):
            print r.content

            print "Got the REST Token: " + r.json()['key']

            self.token = r.json()['key']
            self.headers['authorization'] = "Token " + r.json()['key']

            payload = {"new_password1": "new_person", "new_password2": "wrong_person"}
            print 'Sending a POST request to password change API'

            r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

            if self.assertEqual(r.status_code, 400):
                print r.content

    def test_required_fields_for_password_change(self):
        print 'Logging in'
        payload = {"username": "person", "password": "person"}
        login_url = "http://localhost:8000/rest_auth/login/"

        print 'Sending a POST request to login API'

        r = requests.post(login_url, data=json.dumps(payload), headers=self.headers)

        if self.assertEqual(r.status_code, 200):
            print r.content

            print "Got the REST Token: " + r.json()['key']

            self.token = r.json()['key']
            self.headers['authorization'] = "Token " + r.json()['key']

            payload = {}

            print 'The request will attempt to login with no data provided.'
            print 'Sending a POST request to password change API'

            r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)

            if self.assertEqual(r.status_code, 400):
                print r.content
