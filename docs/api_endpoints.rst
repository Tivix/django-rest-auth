API endpoints
=============

Basic
-----

- /dj-rest-auth/login/ (POST)

    - username
    - email
    - password

    Returns Token key

- /dj-rest-auth/logout/ (POST)

    .. note:: ``ACCOUNT_LOGOUT_ON_GET = True`` to allow logout using GET - this is the exact same configuration from allauth. NOT recommended, see: http://django-allauth.readthedocs.io/en/latest/views.html#logout

- /dj-rest-auth/password/reset/ (POST)

    - email

- /dj-rest-auth/password/reset/confirm/ (POST)

    - uid
    - token
    - new_password1
    - new_password2

    .. note:: uid and token are sent in email after calling /dj-rest-auth/password/reset/

- /dj-rest-auth/password/change/ (POST)

    - new_password1
    - new_password2
    - old_password

    .. note:: ``OLD_PASSWORD_FIELD_ENABLED = True`` to use old_password.
    .. note:: ``LOGOUT_ON_PASSWORD_CHANGE = False`` to keep the user logged in after password change

- /dj-rest-auth/user/ (GET, PUT, PATCH)

    - username
    - first_name
    - last_name

    Returns pk, username, email, first_name, last_name


- /dj-rest-auth/token/verify/ (POST)

    - token

    Returns an empty JSON object.

    .. note:: ``REST_USE_JWT = True`` to use token/verify/ route.
    .. note:: Takes a token and indicates if it is valid.  This view provides no information about a token's fitness for a particular use. Will return a ``HTTP 200 OK`` in case of a valid token and ``HTTP 401 Unauthorized`` with ``{"detail": "Token is invalid or expired", "code": "token_not_valid"}`` in case of a invalid or expired token.


- /dj-rest-auth/token/refresh/ (POST) (`see also <https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#usage>`_)

    - refresh

    Returns access

    .. note:: ``REST_USE_JWT = True`` to use token/refresh/ route.
    .. note:: Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. ``HTTP 401 Unauthorized`` with ``{"detail": "Token is invalid or expired", "code": "token_not_valid"}`` in case of a invalid or expired token.

Registration
------------

- /dj-rest-auth/registration/ (POST)

    - username
    - password1
    - password2
    - email

- /dj-rest-auth/registration/verify-email/ (POST)

    - key

    .. note:: If you set account email verification as mandatory, you have to add the VerifyEmailView with the used `name`.
        You need to import the view: ``from dj_rest_auth.registration.views import VerifyEmailView``. Then add the url with the corresponding name:
        ``path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent')`` to the urlpatterns list.



Social Media Authentication
---------------------------

Basing on example from installation section :doc:`Installation </installation>`

- /dj-rest-auth/facebook/ (POST)

    - access_token
    - code

    .. note:: ``access_token`` OR ``code`` can be used as standalone arguments, see https://github.com/jazzband/dj-rest-auth/blob/master/dj_rest_auth/registration/views.py

- /dj-rest-auth/twitter/ (POST)

    - access_token
    - token_secret
