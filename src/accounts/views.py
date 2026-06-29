from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from django.urls import reverse
from django.contrib import messages

from .forms import RegistrationForm
from task_manage.oauth import oauth
from .models import CustomUser

def register_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("task_manage:dashboard")
    return render(request, "accounts/register.html", {"form": form})


class GoogleLoginView(View):
    def get(self, request):
        callback_path = reverse("accounts:google_callback")
        redirect_url = request.build_absolute_uri(callback_path)
        return oauth.google.authorize_redirect(request, redirect_url)
    

class GoogleCallbackView(View):
    def get(self, request):
        token = oauth.google.authorize_access_token(request)
        response = oauth.google.get(
            "https://openidconnect.googleapis.com/v1/userinfo", token=token
        )
        user_info = response.json()

        email = user_info["email"]
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")
        sub = user_info.get("sub")
        username = email.split("@")[0]

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        )
        user.is_active = True
        user.save()
        user.backend = "django.contrib.auth.backends.ModelBackend"

        login(request, user)

        response = redirect("task_manage:dashboard")
        if created:
            messages.success(request, "Ласкаво просимо! Ви успішно зареєструвалися.")
        else:
            messages.success(request, "З поверненням!")
        return response