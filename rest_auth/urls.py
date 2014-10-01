from django.conf import settings
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from rest_auth.views import Login, Logout, UserDetails, \
    PasswordChange, PasswordReset, PasswordResetConfirm


urlpatterns = patterns('rest_auth.views',
                       # URLs that do not require a session or valid token
                       url(r'^password/reset/$', PasswordReset.as_view(),
                           name='rest_password_reset'),
                       url(r'^password/reset/confirm/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           PasswordResetConfirm.as_view(
                           ), name='rest_password_reset_confirm'),
                       url(r'^login/$', Login.as_view(), name='rest_login'),

                       # URLs that require a user to be logged in with a valid
                       # session / token.
                       url(r'^logout/$', Logout.as_view(), name='rest_logout'),
                       url(r'^user/$', UserDetails.as_view(),
                           name='rest_user_details'),
                       url(r'^password/change/$', PasswordChange.as_view(),
                           name='rest_password_change'),
                       )

if getattr(settings, 'IS_TEST', False):
    from django.contrib.auth.tests import urls
    urlpatterns += patterns('',
        url(r'^rest-registration/', include('registration.urls')),
        url(r'^test-admin/', include(urls)),
        url(r'^account-email-verification-sent/$', TemplateView.as_view(),
            name='account_email_verification_sent'),
        url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
            name='account_confirm_email'),
    )
