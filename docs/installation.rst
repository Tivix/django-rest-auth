Installation
============

1. Install package:

.. code-block:: python

    pip install dj-rest-auth

2. Add ``dj_rest_auth`` app to INSTALLED_APPS in your django settings.py:

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'rest_framework',
        'rest_framework.authtoken',
        ...,
        'dj_rest_auth'
    )


.. note:: This project depends on ``django-rest-framework`` library, so install it if you haven't done yet. Make sure also you have installed ``rest_framework`` and ``rest_framework.authtoken`` apps

3. Add dj_rest_auth urls:

.. code-block:: python

    urlpatterns = [
        ...,
        path('dj-rest-auth/', include('dj_rest_auth.urls'))
    ]

4. Migrate your database

.. code-block:: python

    python manage.py migrate


You're good to go now!


Registration (optional)
-----------------------

1. If you want to enable standard registration process you will need to install ``django-allauth`` by using ``pip install 'dj-rest-auth[with_social]'``.

2. Add ``django.contrib.sites``, ``allauth``, ``allauth.account``, ``allauth.socialaccount`` and ``dj_rest_auth.registration`` apps to INSTALLED_APPS in your django settings.py:

3. Add ``SITE_ID = 1``  to your django settings.py

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'dj_rest_auth.registration',
    )

    SITE_ID = 1

3. Add dj_rest_auth.registration urls:

.. code-block:: python

    urlpatterns = [
        ...,
        path('dj-rest-auth/', include('dj_rest_auth.urls')),
        path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
    ]


Social Authentication (optional)
--------------------------------

Using ``django-allauth``, ``dj-rest-auth`` provides helpful class for creating social media authentication view.

.. note:: Points 1 and 2 are related to ``django-allauth`` configuration, so if you have already configured social authentication, then please go to step 3. See ``django-allauth`` documentation for more details.

1. Add ``allauth.socialaccount`` and ``allauth.socialaccount.providers.facebook`` or ``allauth.socialaccount.providers.twitter`` apps to INSTALLED_APPS in your django settings.py:

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'rest_framework',
        'rest_framework.authtoken',
        'dj_rest_auth'
        ...,
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'dj_rest_auth.registration',
        ...,
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.twitter',

    )

2. Add Social Application in django admin panel

Facebook
########

3. Create new view as a subclass of ``dj_rest_auth.registration.views.SocialLoginView`` with ``FacebookOAuth2Adapter`` adapter as an attribute:

.. code-block:: python

    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
    from dj_rest_auth.registration.views import SocialLoginView

    class FacebookLogin(SocialLoginView):
        adapter_class = FacebookOAuth2Adapter

4. Create url for FacebookLogin view:

.. code-block:: python

    urlpatterns += [
        ...,
        path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login')
    ]


Twitter
#######

If you are using Twitter for your social authentication, it is a bit different since Twitter uses OAuth 1.0.

3. Create new view as a subclass of ``dj_rest_auth.registration.views.SocialLoginView`` with ``TwitterOAuthAdapter`` adapter and  ``TwitterLoginSerializer`` as an attribute:

.. code-block:: python

    from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
    from dj_rest_auth.registration.views import SocialLoginView
    from dj_rest_auth.social_serializers import TwitterLoginSerializer

    class TwitterLogin(SocialLoginView):
        serializer_class = TwitterLoginSerializer
        adapter_class = TwitterOAuthAdapter

4. Create url for TwitterLogin view:

.. code-block:: python

    urlpatterns += [
        ...,
        path('dj-rest-auth/twitter/', TwitterLogin.as_view(), name='twitter_login')
    ]

.. note:: Starting from v0.21.0, django-allauth has dropped support for context processors. Check out http://django-allauth.readthedocs.org/en/latest/changelog.html#from-0-21-0 for more details.


GitHub
######

If you are using GitHub for your social authentication, it uses code and not AccessToken directly.

3. Create new view as a subclass of ``dj_rest_auth.views.SocialLoginView`` with ``GitHubOAuth2Adapter`` adapter, an ``OAuth2Client`` and a callback_url as attributes:

.. code-block:: python

    from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client
    from dj_rest_auth.registration.views import SocialLoginView

    class GithubLogin(SocialLoginView):
        adapter_class = GitHubOAuth2Adapter
        callback_url = CALLBACK_URL_YOU_SET_ON_GITHUB
        client_class = OAuth2Client

4. Create url for GitHubLogin view:

.. code-block:: python

    urlpatterns += [
        ...,
        path('dj-rest-auth/github/', GitHubLogin.as_view(), name='github_login')
    ]

Additional Social Connect Views
###############################

If you want to allow connecting existing accounts in addition to login, you can use connect views:

.. code-block:: python

    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
    from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
    from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client
    from dj_rest_auth.registration.views import SocialConnectView
    from dj_rest_auth.social_serializers import TwitterConnectSerializer

    class FacebookConnect(SocialConnectView):
        adapter_class = FacebookOAuth2Adapter

    class TwitterConnect(SocialConnectView):
        serializer_class = TwitterConnectSerializer
        adapter_class = TwitterOAuthAdapter

    class GithubConnect(SocialConnectView):
        adapter_class = GitHubOAuth2Adapter
        callback_url = CALLBACK_URL_YOU_SET_ON_GITHUB
        client_class = OAuth2Client


In urls.py:

.. code-block:: python

    urlpatterns += [
        ...,
        path('dj-rest-auth/facebook/connect/', FacebookConnect.as_view(), name='fb_connect')
        path('dj-rest-auth/twitter/connect/', TwitterConnect.as_view(), name='twitter_connect')
        path('dj-rest-auth/github/connect/', GithubConnect.as_view(), name='github_connect')
    ]

You can also use the following views to check all social accounts attached to the current authenticated user and disconnect selected social accounts:

.. code-block:: python

    from dj_rest_auth.registration.views import (
        SocialAccountListView, SocialAccountDisconnectView
    )

    urlpatterns += [
        ...,
        path(
            'socialaccounts/',
            SocialAccountListView.as_view(),
            name='social_account_list'
        ),
        path(
            'socialaccounts/<int:pk>/disconnect/',
            SocialAccountDisconnectView.as_view(),
            name='social_account_disconnect'
        )
    ]


JSON Web Token (JWT) Support (optional)
---------------------------------------

By default ``dj-rest-auth`` uses Django's Token-based authentication. If you want to use JWT authentication, follow these steps:

1. Install `djangorestframework-simplejwt <https://github.com/SimpleJWT/django-rest-framework-simplejwt/>`_
    - ``djangorestframework-simplejwt`` is currently the only supported JWT library.

2. Add a simple_jwt auth configuration to the list of authentication classes.

.. code-block:: python

    REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            ...
            'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        )
        ...
    }

3. Add the following configuration value to your settings file to enable JWT authentication in dj-rest-auth.

.. code-block:: python

    REST_USE_JWT = True

4. Declare what you want the cookie key to be called.

.. code-block:: python

    JWT_AUTH_COOKIE = 'my-app-auth'


This example value above will cause dj-rest-auth to return a `Set-Cookie` header that looks like this:

.. code-block:: bash

    Set-Cookie: my-app-auth=xxxxxxxxxxxxx; expires=Sat, 28 Mar 2020 18:59:00 GMT; HttpOnly; Max-Age=300; Path=/

``JWT_AUTH_COOKIE`` is also used while authenticating each request against protected views.
