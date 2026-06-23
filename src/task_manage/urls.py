from django.urls import path
from django.views.generic import RedirectView
from . import views


app_name = 'task_manage'


urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile")
]