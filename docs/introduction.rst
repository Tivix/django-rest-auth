Introduction
============


Since the introduction of django-rest-framework, Django apps have been able to serve up app-level REST API endpoints. As a result, we saw a lot of instances where developers implemented their own REST registration API endpoints here and there, snippets, and so on. We aim to solve this demand by providing django-rest-auth, a set of REST API endpoints to handle User Registration and Authentication tasks. By having these API endpoints, your client apps such as AngularJS, iOS, Android, and others can communicate to your Django backend site independently via REST APIs for User Management. Of course, we'll add more API endpoints as we see the demand.

Features
--------

* User Registration with activation
* Login/Logout
* Retrieve/Update the Django User model
* Password change
* Password reset via e-mail
* Social Media authentication


Apps structure
--------------

* ``rest_auth`` has basic auth functionality like login, logout, password reset and password change
* ``rest_auth.registration`` has logic related with registration and social media authentication


Angular app
-----------

- Tivix has also created angular module which uses API endpoints from this app - `angular-django-registration-auth <https://github.com/Tivix/angular-django-registration-auth>`_


Demo project
------------

- You can also check our :doc:`Demo Project </demo>` which is using jQuery on frontend.
