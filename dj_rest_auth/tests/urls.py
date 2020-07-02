from allauth.socialaccount.providers.facebook.views import \
    FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.registration.views import (SocialAccountDisconnectView,
                                             SocialAccountListView,
                                             SocialConnectView,
                                             SocialLoginView)
from dj_rest_auth.social_serializers import (TwitterConnectSerializer,
                                             TwitterLoginSerializer)
from dj_rest_auth.urls import urlpatterns
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from . import django_urls


class ExampleProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, *args, **kwargs):
        return Response(dict(success=True))

    def post(self, *args, **kwargs):
        return Response(dict(success=True))


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

@ensure_csrf_cookie
@api_view(['GET'])
def get_csrf_cookie(request):
    return Response()


urlpatterns += [
    url(r'^rest-registration/', include('dj_rest_auth.registration.urls')),
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
    url(r'^protected-view/$', ExampleProtectedView.as_view()),
    url(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect'),
    url(r'^accounts/', include('allauth.socialaccount.urls')),
    url(r'^getcsrf/', get_csrf_cookie, name='getcsrf'),
]
