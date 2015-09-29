from django.conf.urls import patterns, url

from django.conf import settings

from rest_auth.views import (
    LoginView, SimpleLoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = patterns(
    '',
    # URLs that do not require a session or valid token
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^password/change/$', PasswordChangeView.as_view(),
        name='rest_password_change'),
)

if getattr(settings, 'USER_DETAILS_INCLUDED', True):
    urlpatterns += patterns(
    '',
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
)

if getattr(settings, 'SIMPLE_LOGIN', False):
    urlpatterns += patterns(
    '',
    url(r'^login/$', SimpleLoginView.as_view(), name='rest_login'),
)
else:
    urlpatterns += patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
)
