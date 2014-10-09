API endpoints
=============

Basic
-----


- (POST) /rest-auth/login/

    - username (string)
    - password (string)


- (POST) /rest-auth/logout/

- (POST) /rest-auth/password/reset/

    - email

- (POST) /rest-auth/password/reset/confim/

    - uid
    - token
    - new_password1
    - new_password2

- (POST) /rest-auth/password/change/

    - new_password1
    - new_password2

- (GET) /rest-auth/user/

- (PUT/PATCH) /rest-auth/user/

    - username
    - first_name
    - last_name
    - email


Registration
------------
