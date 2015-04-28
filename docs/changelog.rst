Changelog
=========

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
