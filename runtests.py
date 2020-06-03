# This file mainly exists to allow python setup.py test to work.
# flake8: noqa
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'dj_rest_auth.tests.settings'
test_dir = os.path.join(os.path.dirname(__file__), 'dj_rest_auth')
sys.path.insert(0, test_dir)



def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    if hasattr(django, 'setup'):
        django.setup()
    failures = test_runner.run_tests(['dj_rest_auth'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
