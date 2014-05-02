from django.conf import settings
from django.conf.urls import patterns, url, include

from rest_auth.views import Login, Logout, Register, UserDetails, \
    PasswordChange, PasswordReset, VerifyEmail, PasswordResetConfirm


urlpatterns = patterns('rest_auth.views',
                       # URLs that do not require a session or valid token
                       url(r'^register/$', Register.as_view(),
                           name='rest_register'),
                       url(r'^password/reset/$', PasswordReset.as_view(),
                           name='rest_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           PasswordResetConfirm.as_view(
                           ), name='rest_password_reset_confirm'),
                       url(r'^login/$', Login.as_view(), name='rest_login'),
                       url(r'^verify-email/(?P<activation_key>\w+)/$',
                           VerifyEmail.as_view(), name='verify_email'),

                       # URLs that require a user to be logged in with a valid
                       # session / token.
                       url(r'^logout/$', Logout.as_view(), name='rest_logout'),
                       url(r'^user/$', UserDetails.as_view(),
                           name='rest_user_details'),
                       url(r'^password/change/$', PasswordChange.as_view(),
                           name='rest_password_change'),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            # Swagger Docs
                            url(r'^docs/',
                                include('rest_framework_swagger.urls')),
                            )
