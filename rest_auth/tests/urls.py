from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import django_urls

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter

from rest_auth.urls import urlpatterns
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_auth.views import LoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(LoginView):
    adapter_class = TwitterOAuthAdapter
    serializer_class = TwitterLoginSerializer


urlpatterns += [
    url(r'^rest-registration/', include('rest_auth.registration.urls')),
    url(r'^test-admin/', include(django_urls)),
    url(r'^account-email-verification-sent/$', TemplateView.as_view(),
        name='account_email_verification_sent'),
    url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
    url(r'^social-login/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^social-login/twitter/$', TwitterLogin.as_view(), name='tw_login'),
    url(r'^accounts/', include('allauth.socialaccount.urls'))
]
