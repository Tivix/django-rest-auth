#This file mainly exists to allow python setup.py test to work.
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.db import models

from rest_framework.serializers import _resolve_model
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from registration import signals

"""
create user profile model
"""
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    newsletter_subscribe = models.BooleanField(default=False)

    class Meta:
        app_label = 'rest_auth'


"""
overwrite register to avoid sending email
"""
class RegistrationView(BaseRegistrationView):
    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site, send_email=False)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        # create user profile
        profile_model_path = getattr(settings, 'REST_PROFILE_MODULE', None)
        if profile_model_path:
            user_profile_model = _resolve_model(profile_model_path)
            user_profile_model.objects.create(user=new_user)

        return new_user


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['rest_auth'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
