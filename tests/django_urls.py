# Moved in Django 1.8 from django to tests/auth_tests/urls.py

from django.conf.urls import url
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns


# special urls for auth test cases
urlpatterns += [
    url(r'^logout/custom_query/$', views.logout, dict(redirect_field_name='follow')),
    url(r'^logout/next_page/$', views.logout, dict(next_page='/somewhere/')),
    url(r'^logout/next_page/named/$', views.logout, dict(next_page='password_reset')),
    url(r'^password_reset_from_email/$', views.password_reset, dict(from_email='staffmember@example.com')),
    url(r'^password_reset/custom_redirect/$', views.password_reset, dict(post_reset_redirect='/custom/')),
    url(r'^password_reset/custom_redirect/named/$', views.password_reset, dict(post_reset_redirect='password_reset')),
    url(r'^password_reset/html_email_template/$', views.password_reset,
        dict(html_email_template_name='registration/html_password_reset_email.html')),
    url(r'^reset/custom/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        dict(post_reset_redirect='/custom/')),
    url(r'^reset/custom/named/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        dict(post_reset_redirect='password_reset')),
    url(r'^password_change/custom/$', views.password_change, dict(post_change_redirect='/custom/')),
    url(r'^password_change/custom/named/$', views.password_change, dict(post_change_redirect='password_reset')),
    url(r'^admin_password_reset/$', views.password_reset, dict(is_admin_site=True)),
    url(r'^login_required/$', login_required(views.password_reset)),
    url(r'^login_required_login_url/$', login_required(views.password_reset, login_url='/somewhere/')),
]
