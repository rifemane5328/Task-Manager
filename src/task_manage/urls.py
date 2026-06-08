from django.urls import path
from . import views


app_name = 'task_manage'


urlpatterns = [
    path("", views.index_view, name="index")
]