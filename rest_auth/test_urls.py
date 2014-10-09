from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.tests import urls

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

from .urls import urlpatterns
from .registration.views import SocialLogin


class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter

urlpatterns += patterns('',
    url(r'^rest-registration/', include('registration.urls')),
    url(r'^test-admin/', include(urls)),
    url(r'^account-email-verification-sent/$', TemplateView.as_view(),
        name='account_email_verification_sent'),
    url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
    url(r'^social-login/facebook/$', FacebookLogin.as_view(), name='fb_login')
)
