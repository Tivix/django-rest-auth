[![Build Status](https://travis-ci.org/Tivix/django-rest-auth.svg?branch=master)](https://travis-ci.org/Tivix/django-rest-auth)  [![Coverage Status](https://coveralls.io/repos/Tivix/django-rest-auth/badge.png?branch=master)](https://coveralls.io/r/Tivix/django-rest-auth?branch=master)

django-rest-auth
================

Since the introduction of django-rest-framework, Django apps have been able to serve up app-level REST API endpoints. As a result, we saw a lot of instances where developers implemented their own REST registration API endpoints here and there, snippets, and so on. We aim to solve this demand by providing django-rest-auth, a set of REST API endpoints to handle User Registration and Authentication tasks. By having these API endpoints, your client apps such as AngularJS, iOS, Android, and others can communicate to your Django backend site independently via REST APIs for User Management. Of course, we'll add more API endpoints as we see the demand.

Features
--------
1. User Registration with activation
2. Login/Logout
3. Retrieve/Update the Django User & user-defined UserProfile model
4. Password change
5. Password reset via e-mail

Installation
------------

1. This project needs the following packages

    > django-registration>=1.0
    >
    > djangorestframework>=2.3.13

2. Install this package

3. Add rest_auth app to INSTALLED\_APPS in your django settings.py

        INSTALLED_APPS = (
            ...,
            'rest_auth',
        )

4. This project depends on django-rest-framework library, therefore the following REST_FRAMEWORK settings needs to be entered in your Django settings.py

        REST_FRAMEWORK = {
                'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.SessionAuthentication',
            ),

            'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework.permissions.IsAuthenticated'
            )
        }

5. Lastly, this project accepts the following Django setting values. You can set the UserProfile model and/or create your own REST registration backend for django-registration

        REST_REGISTRATION_BACKEND = 'rest_auth.backends.rest_registration.RESTRegistrationView'
        REST_PROFILE_MODULE = 'accounts.UserProfile'

6. Add rest_auth urls in your project root urls.py

        urlpatterns = patterns('',
            ...,
            (r'^rest-auth/', include('rest_auth.urls')),
        )

7. You're good to go now!

API endpoints without Authentication
------------------------------------

1. /rest-auth/register/
    - POST
        - username
        - password
        - email
        - first\_name
        - last\_name
2. /rest-auth/password/reset/
    - POST
        - email
3. /rest-auth/password/reset/confirm/{uidb64}/{token}/
    - POST
        - new\_password1
        - new\_password2
4. /rest-auth/login/
    - POST
        - username
        - password
5. /rest-auth/verify-email/{activation\_key}/
    - GET

API endpoints with Authentication
---------------------------------

1. /rest-auth/logout/
    - GET
2. /rest-auth/user/
    - GET & POST
        - POST parameters
            - user as dictionary
            - user-defined UserProfile model fields
            - user data example
                    "user": {"id": 1, "first_name": "Person", "last_name": "2"}

3. /rest-auth/password/change/
    - POST
        - new\_password1
        - new\_password2
