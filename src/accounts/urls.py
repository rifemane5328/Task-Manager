from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'accounts'

urlpatterns = [
    path("", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("register/", views.register_view, name="register")
]