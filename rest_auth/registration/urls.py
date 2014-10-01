from django.conf.urls import patterns, url

from .views import Register, VerifyEmail

urlpatterns = patterns('',
    url(r'^$', Register.as_view(), name='rest_register'),
    url(r'^verify-email/(?P<activation_key>\w+)/$', VerifyEmail.as_view(),
        name='verify_email'),
)

