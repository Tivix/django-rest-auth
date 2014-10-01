from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from allauth.account.views import SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings

from rest_auth.serializers import UserDetailsSerializer


class Register(APIView, SignupView):

    permission_classes = (AllowAny,)
    user_serializer_class = UserDetailsSerializer

    def form_valid(self, form):
        self.user = form.save(self.request)
        return complete_signup(self.request, self.user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.initial = {}
        self.request.POST = self.request.DATA.copy()
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form_valid(self.form)
            return self.get_response()
        else:
            return self.get_response_with_errors()

    def get_response(self):
        serializer = self.user_serializer_class(instance=self.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_response_with_errors(self):
        return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    pass
