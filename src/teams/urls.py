from django.urls import path
from . import views


app_name = "teams"


urlpatterns = [
    path("", views.teams_view, name="my_teams"),
    path("<int:team_id>/tasks/", views.team_tasks_view, name="team_detail"),
    path("tasks/<int:task_id>/edit/", views.team_edit_task_view, name="team_edit_task"),
    path("<int:team_id>/members/", views.team_members_view, name="team_members"),
    path("<int:team_id>/settings/", views.team_settings_view, name="team_settings"),
]