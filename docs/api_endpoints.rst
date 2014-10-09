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

- /rest-auth/password/reset/confim/ (POST)

    - uid
    - token
    - new_password1
    - new_password2

    .. note:: uid and token are sent in email after calling /rest-auth/password/reset/

- /rest-auth/password/change/ (POST)

    - new_password1
    - new_password2

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
    - password1
    - password2
    - email

    .. note:: This endpoint is based on ``allauth.account.views.SignupView`` and uses the same form as in this view. To override fields you have to create custom Signup Form and define it in django settings:

        .. code-block:: python

            ACCOUNT_FORMS = {
                'signup': 'path.to.custom.SignupForm'
            }

        See allauth documentation for more details.

- /rest-auth/registration/ (POST)

    - key


Social Media Authentication
---------------------------

Basing on example from installation section :doc:`Installation </installation>`

- /rest-auth/facebook/ (POST)

    - access_token
