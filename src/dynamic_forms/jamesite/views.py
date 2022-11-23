from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class LoginViews(LoginView):
    template_name = 'login.html'
    login_redirect_url = reverse_lazy('index')

