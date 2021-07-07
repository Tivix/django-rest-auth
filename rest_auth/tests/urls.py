from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import django_urls

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter

from rest_framework.decorators import api_view

from rest_auth.urls import urlpatterns
from rest_auth.registration.views import (
    SocialLoginView, SocialConnectView, SocialAccountListView,
    SocialAccountDisconnectView
)
from rest_auth.social_serializers import (
    TwitterLoginSerializer, TwitterConnectSerializer
)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    adapter_class = TwitterOAuthAdapter
    serializer_class = TwitterLoginSerializer


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class TwitterConnect(SocialConnectView):
    adapter_class = TwitterOAuthAdapter
    serializer_class = TwitterConnectSerializer


class TwitterLoginSerializerFoo(TwitterLoginSerializer):
    pass


@api_view(['POST'])
def twitter_login_view(request):
    serializer = TwitterLoginSerializerFoo(
        data={'access_token': '11223344', 'token_secret': '55667788'},
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)


class TwitterLoginNoAdapter(SocialLoginView):
    serializer_class = TwitterLoginSerializer


urlpatterns += [
    url(r'^rest-registration/', include('rest_auth.registration.urls')),
    url(r'^test-admin/', include(django_urls)),
    url(r'^account-email-verification-sent/$', TemplateView.as_view(),
        name='account_email_verification_sent'),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
    url(r'^social-login/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^social-login/twitter/$', TwitterLogin.as_view(), name='tw_login'),
    url(r'^social-login/twitter-no-view/$', twitter_login_view, name='tw_login_no_view'),
    url(r'^social-login/twitter-no-adapter/$', TwitterLoginNoAdapter.as_view(), name='tw_login_no_adapter'),
    url(r'^social-login/facebook/connect/$', FacebookConnect.as_view(), name='fb_connect'),
    url(r'^social-login/twitter/connect/$', TwitterConnect.as_view(), name='tw_connect'),
    url(r'^socialaccounts/$', SocialAccountListView.as_view(), name='social_account_list'),
    url(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect'),
    url(r'^accounts/', include('allauth.socialaccount.urls'))
]
