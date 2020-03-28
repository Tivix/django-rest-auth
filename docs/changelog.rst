Changelog
=========

0.1.2
-----
Welcome Dj-Rest-Auth

1.0.0
-----
Replaces `rest_framework_jwt` with `djangorestframework-simplejwt`.


- rest_framework_jwt is now unmaintained so we've switched to simplewjt,
which is a strong jwt library with a large community.
- This change means you may need to change your client code if you're upgrading
  from the previous version. Example: token -> access_token. Please see demo
  for more information.