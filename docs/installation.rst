Installation
============

1. Add ``rest_auth`` app to INSTALLED_APPS in your django settings.py:

.. code-block:: python
   :emphasize-lines: 3,5

    INSTALLED_APPS = (
        ...,
        'rest_framework',
        'rest_framework.authtoken',
        ...,
        'rest_auth'
    )


.. note:: This project depends on ``django-rest-framework`` library, so install it if you haven't done yet. Make sure also you have installed ``rest_framework`` and ``rest_framework.authtoken`` apps

2. Add rest_auth urls:

.. code-block:: python
   :emphasize-lines: 3,5

    urlpatterns = patterns('',
        ...,
        (r'^rest-auth/', include('rest_auth.urls'))
    )


You're good to go now!


Registration (optional)
-----------------------

1. If you want to enable standard registration process you will need to install ``django-allauth`` - see this doc for installation http://django-allauth.readthedocs.org/en/latest/installation.html.

2. Add ``allauth``, ``allauth.account`` and ``rest_auth.registration`` apps to INSTALLED_APPS in your django settings.py:

.. code-block:: python
   :emphasize-lines: 3,5

    INSTALLED_APPS = (
        ...,
        'allauth',
        'allauth.account',
        'rest_auth.registration',
    )

3. Add rest_auth.registration urls:

.. code-block:: python
   :emphasize-lines: 3,5

    urlpatterns = patterns('',
        ...,
        (r'^rest-auth/', include('rest_auth.urls'))
        (r'^rest-auth/registration/', include('rest_auth.registration.urls'))
    )


Social Authenitcation (optional)
--------------------------------

Using ``django-allauth``, ``django-rest-auth`` provides helpful class for creating social media authentication view. Below is an example with Facebook authentication.

1. Add ``allauth.socialaccount`` and ``allauth.socialaccount.providers.facebook`` apps to INSTALLED_APPS in your django settings.py:

.. code-block:: python
   :emphasize-lines: 3,5

    INSTALLED_APPS = (
        ...,
        'rest_framework',
        'rest_framework.authtoken',
        'rest_auth'
        ...,
        'allauth',
        'allauth.account',
        'rest_auth.registration',
        ...,
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
    )

2. Create a view as a subclass of ``rest_auth.registration.views.SocialLogin``:

.. code-block:: python
   :emphasize-lines: 3,5

    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
    from rest_auth.registration.views import SocialLogin

    class FacebookLogin(SocialLogin):
        adapter_class = FacebookOAuth2Adapter

3. Create url for FacebookLogin view:

.. code-block:: python
   :emphasize-lines: 3,5

    urlpatterns += pattern('',
        ...,
        url(r'^social-login/facebook/$', FacebookLogin.as_view(), name='fb_login')
    )
