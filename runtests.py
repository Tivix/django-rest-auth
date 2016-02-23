# This file mainly exists to allow python setup.py test to work.
# flake8: noqa
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
test_dir = os.path.join(os.path.dirname(__file__), 'rest_auth')
sys.path.insert(0, test_dir)

import django
from django.test.utils import get_runner
from django.conf import settings


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    if hasattr(django, 'setup'):
        django.setup()
    failures = test_runner.run_tests(['rest_auth'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
