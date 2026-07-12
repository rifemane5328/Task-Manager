from django.urls import path
from . import views


app_name = "teams"


urlpatterns = [
    path("", views.teams_view, name="my_teams"),
    path("<int:team_id>/detail", views.team_detail_view, name="team_detail")
]