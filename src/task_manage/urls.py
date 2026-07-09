from django.urls import path
from django.views.generic import RedirectView
from . import views


app_name = 'task_manage'


urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("my-tasks/", views.my_tasks_view, name="my_tasks"),
    path("edit-task/<int:task_id>/", views.edit_task_view, name="edit_task"),
]