from django.conf import settings
from django.conf.urls import url

from rest_auth.views import (
    LoginView, LogoutView, LogoutAllView, UserDetailsView,
    PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    # URLs that do not require a session or valid token
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^password/change/$', PasswordChangeView.as_view(),
        name='rest_password_change'),
]

if getattr(settings, 'REST_USE_KNOX', False):
    urlpatterns.append(
        url(r'^logoutall/$', LogoutAllView.as_view(), name='rest_logout_all')
    )
