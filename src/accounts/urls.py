from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from . import views

app_name = 'accounts'

urlpatterns = [
    path("", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("google/login/", views.GoogleLoginView.as_view(), name="google_login"),
    path("google/callback/", views.GoogleCallbackView.as_view(), name="google_callback"),
]