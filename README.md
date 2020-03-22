# Dj-Rest-Auth
[![<iMerica>](https://circleci.com/gh/jazzband/dj-rest-auth.svg?style=svg)](https://app.circleci.com/github/jazzband/dj-rest-auth/pipelines)
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




### Documentation

View the full documentation here: https://dj-rest-auth.readthedocs.io/en/latest/index.html


### Acknowledgements

This project began as a fork of `django-rest-auth`. Big thanks to everyone who contributed to that repo!