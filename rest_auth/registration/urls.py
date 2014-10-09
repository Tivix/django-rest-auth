from django.views.generic import TemplateView
from django.conf.urls import patterns, url

from .views import Register, VerifyEmail

urlpatterns = patterns('',
    url(r'^$', Register.as_view(), name='rest_register'),
    url(r'^verify-email/$', VerifyEmail.as_view(), name='verify_email'),

    url(r'^account-email-verification-sent/$', TemplateView.as_view(),
        name='account_email_verification_sent'),
    url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
        name='account_confirm_email'),

)

