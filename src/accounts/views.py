from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def register_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_vaid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            response = redirect("task_manage:profile")
    return render(request, "accounts/register.html", {"form": form})