API endpoints
=============

Basic
-----

Typically, auth data is sent in the body, with a header ``Content-Type: application/x-www-form-urlencoded``

/rest-auth/login/ (POST)
************************
**Request (standalone):**

- ``username`` or ``email`` (email will be used to lookup username)
- ``password`` (required)

**Request (using django-allauth):**

- ``username`` (required when ``ACCOUNT_AUTHENTICATION_METHOD = 'username'`` or ``'username_email'``)
- ``email`` (required when ``ACCOUNT_AUTHENTICATION_METHOD = 'email'`` or ``'username_email'``)
- ``password`` (required)

**Response:**

- ``token``
- ``user`` (when using django-rest-framework-jwt or django-rest-knox)

/rest-auth/logout/ (POST)
*************************
    
**Request (standalone):**

- No values expected

**Request (using django-rest-knox):**

- ``Authorization: Token TOKEN`` *(Header)*

**Response:**

- No values

.. note:: ``ACCOUNT_LOGOUT_ON_GET = True`` to allow logout using GET - this is the exact same configuration from allauth. NOT recommended, see: http://django-allauth.readthedocs.io/en/latest/views.html#logout

/rest-auth/logoutall/ (POST)
****************************

This endpoint deletes all Knox tokens, and will only be loaded when `REST_USE_KNOX = True`.   

| **Request (using django-rest-knox):**

- `Authorization`: `Token TOKEN` (Header)

**Response:**

- No values

.. note:: ``ACCOUNT_LOGOUT_ON_GET = True`` to allow logout using GET - this is the exact same configuration from allauth. NOT recommended, see: http://django-allauth.readthedocs.io/en/latest/views.html#logout

/rest-auth/password/reset/ (POST)
*********************************

- email

/rest-auth/password/reset/confirm/ (POST)
*****************************************

- uid
- token
- new_password1
- new_password2

.. note:: uid and token are sent in email after calling /rest-auth/password/reset/

/rest-auth/password/change/ (POST)
**********************************
- new_password1
- new_password2
- old_password

.. note:: ``OLD_PASSWORD_FIELD_ENABLED = True`` to use old_password.
.. note:: ``LOGOUT_ON_PASSWORD_CHANGE = False`` to keep the user logged in after password change

/rest-auth/user/ (GET, PUT, PATCH)
**********************************
- username
- first_name
- last_name

Returns pk, username, email, first_name, last_name


Registration
------------

/rest-auth/registration/ (POST)
*******************************

**Request (using django-allauth):**

- ``username`` (required when ``ACCOUNT_AUTHENTICATION_METHOD = 'username'`` or ``'username_email'``, or when ``ACCOUNT_USERNAME_REQUIRED = True``)
- ``email`` (required when ``ACCOUNT_AUTHENTICATION_METHOD = 'email'`` or ``'username_email'``, or when ``ACCOUNT_EMAIL_REQUIRED = True``)
- ``password1`` (required)
- ``password2`` (required)

**Response (using django-allauth):**

- No values

**Response (using django-allauth and django-rest-knox)**

- ``token``
- ``user``

/rest-auth/registration/verify-email/ (POST)
********************************************

**Request (using django-allauth):**

- ``key``

**Response (using django-allauth):**

- No values

Social Media Authentication
---------------------------

Based on the example from the installation section :doc:`Installation </installation>`

/rest-auth/facebook/ (POST)
***************************

- ``access_token``
- ``code``

    .. note:: ``access_token`` OR ``code`` can be used as standalone arguments, see https://github.com/Tivix/django-rest-auth/blob/master/rest_auth/registration/views.py

/rest-auth/twitter/ (POST)
**************************

- ``access_token``
- ``token_secret``
