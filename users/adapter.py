from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/"
        return path.format(username=request.user.username)

    def get_logout_redirect_url(self, request):
        redirect('/')

    def get_connect_redirect_url(self, request, socialaccount):
        redirect('/')

    def signup(self, request):
        redirect('/')
