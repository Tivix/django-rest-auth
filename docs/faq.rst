FAQ
===

1. Why account_confirm_email url is defined but it is not usable?

    In /rest_auth/registration/urls.py we can find something like this:

    .. code-block:: python

        url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
            name='account_confirm_email'),

    This url is used by django-allauth. Empty TemplateView is defined just to allow reverse() call inside app - when email with verification link is being sent.

    You should override this view/url to handle it in your API client somehow and then, send post to /verify-email/ endpoint with proper key.
    If you don't want to use API on that step, then just use ConfirmEmailView view from:
    djang-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py#L190
