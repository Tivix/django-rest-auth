Configuration
=============

- **REST_AUTH_SERIALIZERS**

    You can define your custom serializers for each endpoint without overriding urls and views by adding ``REST_AUTH_SERIALIZERS`` dictionary in your django settings.
    Possible key values:

        - LOGIN_SERIALIZER - serializer class in ``rest_auth.views.LoginView``, default value ``rest_auth.serializers.LoginSerializer``

        - TOKEN_SERIALIZER - response for successful authentication in ``rest_auth.views.LoginView``, default value ``rest_auth.serializers.TokenSerializer``

        - JWT_SERIALIZER - (Using REST_USE_JWT=True) response for successful authentication in ``rest_auth.views.LoginView``, default value ``rest_auth.serializers.JWTSerializer``

        - USER_DETAILS_SERIALIZER - serializer class in ``rest_auth.views.UserDetailsView``, default value ``rest_auth.serializers.UserDetailsSerializer``

        - PASSWORD_RESET_SERIALIZER - serializer class in ``rest_auth.views.PasswordResetView``, default value ``rest_auth.serializers.PasswordResetSerializer``

        - PASSWORD_RESET_CONFIRM_SERIALIZER - serializer class in ``rest_auth.views.PasswordResetConfirmView``, default value ``rest_auth.serializers.PasswordResetConfirmSerializer``

        - PASSWORD_CHANGE_SERIALIZER - serializer class in ``rest_auth.views.PasswordChangeView``, default value ``rest_auth.serializers.PasswordChangeSerializer``


    Example configuration:

    .. code-block:: python

        REST_AUTH_SERIALIZERS = {
            'LOGIN_SERIALIZER': 'path.to.custom.LoginSerializer',
            'TOKEN_SERIALIZER': 'path.to.custom.TokenSerializer',
            ...
        }

- **REST_AUTH_REGISTER_SERIALIZERS**

    You can define your custom serializers for registration endpoint.
    Possible key values:

        - REGISTER_SERIALIZER - serializer class in ``rest_auth.registration.views.RegisterView``, default value ``rest_auth.registration.serializers.RegisterSerializer``
    
        .. note:: The custom REGISTER_SERIALIZER must define a ``def save(self, request)`` method that returns a user model instance

- **REST_AUTH_TOKEN_MODEL** - model class for tokens, default value ``rest_framework.authtoken.models``

- **REST_AUTH_TOKEN_CREATOR** - callable to create tokens, default value ``rest_auth.utils.default_create_token``.

- **REST_SESSION_LOGIN** - Enable session login in Login API view (default: True)

- **REST_USE_JWT** - Enable JWT Authentication instead of Token/Session based. This is built on top of django-rest-framework-jwt http://getblimp.github.io/django-rest-framework-jwt/, which must also be installed. (default: False)

- **OLD_PASSWORD_FIELD_ENABLED** - set it to True if you want to have old password verification on password change enpoint (default: False)

- **LOGOUT_ON_PASSWORD_CHANGE** - set to False if you want to keep the current user logged in after a password change
