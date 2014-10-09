Changelog
=========

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
