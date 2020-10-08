Configuration
=============

- **REST_AUTH_SERIALIZERS**

    You can define your custom serializers for each endpoint without overriding urls and views by adding ``REST_AUTH_SERIALIZERS`` dictionary in your django settings.
    Possible key values:

        - LOGIN_SERIALIZER - serializer class in ``dj_rest_auth.views.LoginView``, default value ``dj_rest_auth.serializers.LoginSerializer``

        - TOKEN_SERIALIZER - response for successful authentication in ``dj_rest_auth.views.LoginView``, default value ``dj_rest_auth.serializers.TokenSerializer``

        - JWT_SERIALIZER - (Using REST_USE_JWT=True) response for successful authentication in ``dj_rest_auth.views.LoginView``, default value ``dj_rest_auth.serializers.JWTSerializer``

        - JWT_TOKEN_CLAIMS_SERIALIZER - A custom JWT Claim serializer. Default is ``rest_framework_simplejwt.serializers.TokenObtainPairSerializer``

        - USER_DETAILS_SERIALIZER - serializer class in ``dj_rest_auth.views.UserDetailsView``, default value ``dj_rest_auth.serializers.UserDetailsSerializer``

        - PASSWORD_RESET_SERIALIZER - serializer class in ``dj_rest_auth.views.PasswordResetView``, default value ``dj_rest_auth.serializers.PasswordResetSerializer``

        - PASSWORD_RESET_CONFIRM_SERIALIZER - serializer class in ``dj_rest_auth.views.PasswordResetConfirmView``, default value ``dj_rest_auth.serializers.PasswordResetConfirmSerializer``

        - PASSWORD_CHANGE_SERIALIZER - serializer class in ``dj_rest_auth.views.PasswordChangeView``, default value ``dj_rest_auth.serializers.PasswordChangeSerializer``


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

        - REGISTER_SERIALIZER - serializer class in ``dj_rest_auth.registration.views.RegisterView``, default value ``dj_rest_auth.registration.serializers.RegisterSerializer``
    
        .. note:: The custom REGISTER_SERIALIZER must define a ``def save(self, request)`` method that returns a user model instance
- **REST_AUTH_REGISTER_PERMISSION_CLASSES** - A tuple contains paths of another permission classes you wish to be used in ``RegisterView``, ``AllowAny`` is included by default.

    Example :

    .. code-block:: python

        REST_AUTH_REGISTER_PERMISSION_CLASSES = (
            'rest_framework.permissions.IsAuthenticated',
            'path.to.another.permission.class',
            ...
        )
- **REST_AUTH_TOKEN_MODEL** - path to model class for tokens, default value ``'rest_framework.authtoken.models.Token'``
- **REST_AUTH_TOKEN_CREATOR** - path to callable or callable for creating tokens, default value ``dj_rest_auth.utils.default_create_token``.
- **REST_SESSION_LOGIN** - Enable session login in Login API view (default: True)
- **REST_USE_JWT** - Enable JWT Authentication instead of Token/Session based. This is built on top of djangorestframework-simplejwt https://github.com/SimpleJWT/django-rest-framework-simplejwt, which must also be installed. (default: False)
- **JWT_AUTH_COOKIE** - The cookie name/key.
- **JWT_AUTH_SECURE** - If you want the cookie to be only sent to the server when a request is made with the https scheme (default: False).
- **JWT_AUTH_HTTPONLY** - If you want to prevent client-side JavaScript from having access to the cookie (default: True).
- **JWT_AUTH_SAMESITE** - To tell the browser not to send this cookie when performing a cross-origin request (default: 'Lax'). SameSite isn’t supported by all browsers.
- **OLD_PASSWORD_FIELD_ENABLED** - set it to True if you want to have old password verification on password change enpoint (default: False)
- **LOGOUT_ON_PASSWORD_CHANGE** - set to False if you want to keep the current user logged in after a password change
- **JWT_AUTH_COOKIE_USE_CSRF** -  Enables CSRF checks for only authenticated views when using the JWT cookie for auth. Does not effect a client's ability to authenticate using a JWT Bearer Auth header without a CSRF token.
- **JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED** - Enables CSRF checks for authenticated and unauthenticated views when using the JWT cookie for auth. It does not effect a client's ability to authenticate using a JWT Bearer Auth header without a CSRF token (though getting the JWT token in the first place without passing a CSRF token isnt possible).
