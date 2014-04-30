django-rest-auth
=====

Since the introduction of django-rest-framework, Django apps have been able to serve up app-level REST API endpoints. As a result, we saw a lot of instances where developers implemented their own REST registration API endpoints here and there, snippets, and so on. We aim to solve this demand by providing django-rest-auth, a set of REST API endpoints to handle User Registration and Authentication tasks. By having these API endpoints, your client apps such as AngularJS, iOS, Android, and others can communicate to your Django backend site independently via REST APIs for User Management. Of course, we'll add more API endpoints as we see the demand.

Features
--------
1. User Registration with activation
2. Login/Logout
3. Retrieve/Update the Django User & user-defined UserProfile model
4. Password change
5. Password reset via e-mail

Installation
-----------

1. This project needs the following packages

    > django-registration>=1.0
    >
    > djangorestframework>=2.3.13
    >
    > django-rest-swagger>=0.1.14

2. Install this package.

3. Add rest_auth app to INSTALLED\_APPS in your django settings.py

    > INSTALLED\_APPS = (
    >
    >     ...,
    >
    >     'rest_auth',
    > )

4. This project depends on django-rest-framework library, therefore the following REST_FRAMEWORK settings needs to be entered in your Django settings.py::

    > REST_FRAMEWORK = {
    >
    >     'DEFAULT_AUTHENTICATION_CLASSES': (
    >        'rest_framework.authentication.SessionAuthentication',
    >     ),
    >
    >     'DEFAULT_PERMISSION_CLASSES': (
    >         'rest_framework.permissions.IsAuthenticated'
    >     )
    > }

5. Lastly, this project accepts the following Django setting values. You can set the UserProfile model and/or create your own REST registration backend for django-registration.

    > REST\_REGISTRATION\_BACKEND = 'rest\_auth.backends.rest\_registration.RESTRegistrationView'
    >
    > REST\_PROFILE\_MODULE = 'accounts.UserProfile'

6. You're good to go now!

API endpoints without Authentication
------------------------------------

1. /rest\_accounts/register/ - POST

    Parameters

    username, password, email, first\_name, last\_name

2. /rest\_accounts/password/reset/ - POST

    Parameters

    email

3. /rest\_accounts/password/reset/confirm/{uidb64}/{token}/ - POST

    Django URL Keywords

    uidb64, token

    Parameters

    new\_password1, new\_password2

4. /rest\_accounts/login/ - POST

    Parameters

    username, password

5. /rest\_accounts/verify-email/{activation\_key}/ - GET

    Django URL Keywords

    activation_key

API endpoints with Authentication
------------------------------------

1. /rest\_accounts/logout/ - GET

2. /rest\_accounts/user/ - GET & POST

    GET Parameters

    POST Parameters

   user as dictionary with id, email, first\_name, last\_name

   Ex) "user": {"id": 1, "first\_name": "Person", "last\_name": "2"}

   user-defined UserProfile model fields

3. /rest\_accounts/password/change/ - POST

    Parameters

    new\_password1, new\_password2
