# Moved in Django 1.8 from django to tests/auth_tests/urls.py

from django.conf.urls import url
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns

# special urls for auth test cases
urlpatterns += [
    url(r'^logout/custom_query/$',
        views.LogoutView.as_view(redirect_field_name='follow')),
    url(r'^logout/next_page/$',
        views.LogoutView.as_view(next_page='/somewhere/')),
    url(r'^logout/next_page/named/$',
        views.LogoutView.as_view(next_page='password_reset')),
    url(r'^password_reset_from_email/$',
        views.PasswordResetView.as_view(from_email='staffmember@example.com')),
    url(r'^password_reset/custom_redirect/$',
        views.PasswordResetView.as_view(success_url='/custom/')),
    url(r'^password_reset/custom_redirect/named/$',
        views.PasswordResetView.as_view(success_url='password_reset')),
    url(r'^password_reset/html_email_template/$',
        views.PasswordResetView.as_view(html_email_template_name='registration/html_password_reset_email.html')),
    url(r'^reset/custom/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(success_url='/custom/')),
    url(r'^reset/custom/named/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(success_url='password_reset')),
    url(r'^password_change/custom/$',
        views.PasswordChangeView.as_view(success_url='/custom/')),
    url(r'^password_change/custom/named/$',
        views.PasswordChangeView.as_view(success_url='password_reset')),
    url(r'^login_required/$',
        login_required(views.PasswordResetView.as_view())),
    url(r'^login_required_login_url/$',
        login_required(views.PasswordResetView.as_view(), login_url='/somewhere/')),
]
