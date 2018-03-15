from django.views.generic import TemplateView
from django.conf.urls import url

from .views import RegisterView, VerifyEmailView


from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import RedirectView
class ConfirmEmailRedirectView(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        current_site = get_current_site(self.request)
        self.url =  '%s://%s/auth/confirm-email/%s' % (self.request.scheme,current_site.domain, kwargs["key"])
        return super().get_redirect_url(*args, **kwargs)

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='rest_register'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailRedirectView.as_view(),name='account_confirm_email'),
]
