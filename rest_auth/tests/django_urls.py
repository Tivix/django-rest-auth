# Moved in Django 1.8 from django to tests/auth_tests/urls.py

from django.urls import re_path
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns


# special urls for auth test cases
urlpatterns += [
    re_path(r'^logout/custom_query/$', views.logout, dict(redirect_field_name='follow')),
    re_path(r'^logout/next_page/$', views.logout, dict(next_page='/somewhere/')),
    re_path(r'^logout/next_page/named/$', views.logout, dict(next_page='password_reset')),
    re_path(r'^password_reset_from_email/$', views.password_reset, dict(from_email='staffmember@example.com')),
    re_path(r'^password_reset/custom_redirect/$', views.password_reset, dict(post_reset_redirect='/custom/')),
    re_path(r'^password_reset/custom_redirect/named/$', views.password_reset, dict(post_reset_redirect='password_reset')),
    re_path(r'^password_reset/html_email_template/$', views.password_reset,
        dict(html_email_template_name='registration/html_password_reset_email.html')),
    re_path(r'^reset/custom/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        dict(post_reset_redirect='/custom/')),
    re_path(r'^reset/custom/named/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        dict(post_reset_redirect='password_reset')),
    re_path(r'^password_change/custom/$', views.password_change, dict(post_change_redirect='/custom/')),
    re_path(r'^password_change/custom/named/$', views.password_change, dict(post_change_redirect='password_reset')),
    re_path(r'^admin_password_reset/$', views.password_reset, dict(is_admin_site=True)),
    re_path(r'^login_required/$', login_required(views.password_reset)),
    re_path(r'^login_required_login_url/$', login_required(views.password_reset, login_url='/somewhere/')),
]
