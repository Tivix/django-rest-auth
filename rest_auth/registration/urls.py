from django.views.generic import TemplateView
from django.conf.urls import patterns, url

from .views import Register, VerifyEmail

urlpatterns = patterns('',
    url(r'^$', Register.as_view(), name='rest_register'),
    url(r'^verify-email/$', VerifyEmail.as_view(), name='rest_verify_email'),

    # These two views are used in django-allauth and empty TemplateView were
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # djang-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py#L190
    url(r'^account-email-verification-sent/$', TemplateView.as_view(),
        name='account_email_verification_sent'),
    url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
)

