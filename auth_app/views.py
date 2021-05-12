from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import VideoUserCreationForm, VideoUserLoginForm


class RegisterCreateView(CreateView):
    """Регистрация нового пользователя"""
    template_name = 'auth_app/register.html'
    form_class = VideoUserCreationForm
    success_url = reverse_lazy('auth_app:login')


class SignInLoginView(LoginView):
    """Вход в учетную запись пользователя"""
    authentication_form = VideoUserLoginForm
    template_name = 'auth_app/login.html'


class SingOutLogoutView(LogoutView):
    """Выход из учетной записи пользователя"""