FAQ
===

1. Why account_confirm_email url is defined but it is not usable?

    In /rest_auth/registration/urls.py we can find something like this:

    .. code-block:: python

        url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
            name='account_confirm_email'),

    This url is used by django-allauth. Empty TemplateView is defined just to allow reverse() call inside app - when email with verification link is being sent.

    You should override this view/url to handle it in your API client somehow and then, send post to /verify-email/ endpoint with proper key.
    If you don't want to use API on that step, then just use ConfirmEmailView view from:
    django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py


2. I get an error: Reverse for 'password_reset_confirm' not found.

    You need to add `password_reset_confirm` url into your ``urls.py`` (at the top of any other included urls). Please check the ``urls.py`` module inside demo app example for more details.


3. How can I update UserProfile assigned to User model?

    Assuming you already have UserProfile model defined like this

    .. code-block:: python

        from django.db import models
        from django.contrib.auth.models import User

        class UserProfile(models.Model):
            user = models.OneToOneField(User)
            # custom fields for user
            company_name = models.CharField(max_length=100)

    To allow update user details within one request send to rest_auth.views.UserDetailsView view, create serializer like this:

    .. code-block:: python

        from rest_framework import serializers
        from rest_auth.serializers import UserDetailsSerializer

        class UserSerializer(UserDetailsSerializer):

            company_name = serializers.CharField(source="userprofile.company_name")

            class Meta(UserDetailsSerializer.Meta):
                fields = UserDetailsSerializer.Meta.fields + ('company_name',)

            def update(self, instance, validated_data):
                profile_data = validated_data.pop('userprofile', {})
                company_name = profile_data.get('company_name')

                instance = super(UserSerializer, self).update(instance, validated_data)

                # get and update user profile
                profile = instance.userprofile
                if profile_data and company_name:
                    profile.company_name = company_name
                    profile.save()
                return instance

    And setup USER_DETAILS_SERIALIZER in django settings:

    .. code-block:: python

        REST_AUTH_SERIALIZERS = {
            'USER_DETAILS_SERIALIZER': 'demo.serializers.UserSerializer'
        }
