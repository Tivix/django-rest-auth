Changelog
=========

0.8.2
-----
- fixed allauth import error
- added swagger docs to demo project

0.8.1
-----
- added support for django-allauth hmac email confirmation pattern

0.8.0
-----
- added support for django-rest-framework-jwt
- bugfixes

0.7.0
-----
- Wrapped API returned strings in ugettext_lazy
- Fixed not using ``get_username`` which caused issues when using custom user model without username field
- Django 1.9 support
- Added ``TwitterLoginSerializer``

0.6.0
-----
- dropped support for Python 2.6
- dropped support for Django 1.6
- fixed demo code
- added better validation support for serializers
- added optional logout after password change
- compatibility fixes
- bugfixes

0.5.0
-----
- replaced request.DATA with request.data for compatibility with DRF 3.2
- authorization codes for social login
- view classes rename (appended "View" to all of them)
- bugfixes

0.4.0
-----
- Django 1.8 compatiblity fixes

0.3.4
-----
- fixed bug in PasswordResetConfirmation serializer (token field wasn't validated)
- fixed bug in Register view

0.3.3
-----

- support django-rest-framework v3.0

0.3.2
-----

- fixed few minor bugs

0.3.1
-----

- added old_password field in PasswordChangeSerializer
- make all endpoints browsable
- removed LoggedInRESTAPIView, LoggedOutRESTAPIView
- fixed minor bugs

0.3.0
-----

- replaced ``django-registration`` with ``django-allauth``
- moved registration logic to separated django application (``rest_auth.registration``)
- added serializers customization in django settings
- added social media authentication view
- changed request method from GET to POST in logout endpoint
- changed request method from POST to PUT/PATCH for user details edition
- changed password reset confim url - uid and token should be sent in POST
- increase test coverage
- made compatibile with django 1.7
- removed user profile support
