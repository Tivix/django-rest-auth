from dj_rest_auth.views import (LoginView, LogoutView, PasswordChangeView,
                                PasswordResetConfirmView, PasswordResetView,
                                UserDetailsView)
from django.conf.urls import url
from django.conf import settings

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

if getattr(settings, 'REST_USE_JWT', False):
    from rest_framework_simplejwt.views import (
        TokenRefreshView, TokenVerifyView,
    )

    urlpatterns += [
        url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
        url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    ]
