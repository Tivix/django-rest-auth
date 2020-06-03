# Dj-Rest-Auth
[![<iMerica>](https://circleci.com/gh/jazzband/dj-rest-auth.svg?style=svg)](https://app.circleci.com/pipelines/github/jazzband/dj-rest-auth)
[![Jazzband](https://jazzband.co/static/img/badge.svg)](https://jazzband.co/)
[![Coverage Status](https://coveralls.io/repos/github/jazzband/dj-rest-auth/badge.svg?branch=master)](https://coveralls.io/github/jazzband/dj-rest-auth?branch=master)

Drop-in API endpoints for handling authentication securely in Django Rest Framework. Works especially well 
with SPAs (e.g React, Vue, Angular), and Mobile applications. 

## Requirements
- Django 2 or 3.
- Python 3

## Quick Setup

Install package

    pip install dj-rest-auth
    
Add `dj_rest_auth` app to INSTALLED_APPS in your django settings.py:

```python
INSTALLED_APPS = (
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    ...,
    'dj_rest_auth'
)
```
    
Add URL patterns

```python
urlpatterns = [
    url(r'^dj-rest-auth/', include('dj_rest_auth.urls'))
]
```
    

(Optional) Use Http-Only cookies

```python
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'
```

### Testing

To run the tests within a virtualenv, run `python runtests.py` from the repository directory.
The easiest way to run test coverage is with [`coverage`](https://pypi.org/project/coverage/),
which runs the tests against all supported Django installs. To run the test coverage 
within a virtualenv, run `coverage run ./runtests.py` from the repository directory then run `coverage report`.

#### Tox

Testing may also be done using [`tox`](https://pypi.org/project/tox/), which
will run the tests against all supported combinations of python and django.

Install tox, either globally or within a virtualenv, and then simply run `tox`
from the repository directory. As there are many combinations, you may run them
in [`parallel`](https://tox.readthedocs.io/en/latest/config.html#cmdoption-tox-p)
using `tox --parallel`.

The `tox.ini` includes an environment for testing code [`coverage`](https://pypi.org/project/coverage/)
and you can run it and view this report with `tox -e coverage`.

Linting may also be performed via [`flake8`](https://pypi.org/project/flake8/)
by running `tox -e flake8`.

### Documentation

View the full documentation here: https://dj-rest-auth.readthedocs.io/en/latest/index.html


### Acknowledgements

This project began as a fork of `django-rest-auth`. Big thanks to everyone who contributed to that repo!
