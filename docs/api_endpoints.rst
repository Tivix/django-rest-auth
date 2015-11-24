API endpoints
=============

Basic
-----

- /rest-auth/login/ (POST)

    - username (string)
    - password (string)


- /rest-auth/logout/ (POST)

- /rest-auth/password/reset/ (POST)

    - email

- /rest-auth/password/reset/confirm/ (POST)

    - uid
    - token
    - new_password1
    - new_password2

    .. note:: uid and token are sent in email after calling /rest-auth/password/reset/

- /rest-auth/password/change/ (POST)

    - new_password1
    - new_password2
    - old_password


    .. note:: ``OLD_PASSWORD_FIELD_ENABLED = True`` to use old_password.
    .. note:: ``LOGOUT_ON_PASSWORD_CHANGE = False`` to keep the user logged in after password change

- /rest-auth/user/ (GET)

- /rest-auth/user/ (PUT/PATCH)

    - username
    - first_name
    - last_name
    - email


Registration
------------

- /rest-auth/registration/ (POST)

    - username
    - password
    - email

- /rest-auth/registration/verify-email/ (POST)

    - key


Social Media Authentication
---------------------------

Basing on example from installation section :doc:`Installation </installation>`

- /rest-auth/facebook/ (POST)

    - access_token
    - code
