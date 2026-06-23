from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Subquery, OuterRef
from datetime import date

from .models import Task
from teams.models import Team, TeamMember

@login_required
def profile_view(request):
    return render(request, "task_manage/profile.html")

@login_required
def dashboard_view(request):
    base_tasks = Task.objects.filter(assigned_to=request.user, deadline__gte=date.today())

    total_tasks = base_tasks.count()
    user_tasks = base_tasks.order_by("deadline")[:5]
    in_progress = base_tasks.filter(status="in_progress").count()
    missed = Task.objects.filter(assigned_to=request.user, deadline__lt=date.today()).exclude(status="done").count()

    teams = (Team.objects.filter(members__user=request.user).annotate(member_count=Count("members", distinct=True)).annotate(
        user_role=Subquery(TeamMember.objects.filter(team=OuterRef("pk"), user=request.user).values("role")[:1])
    ).annotate(task_count=Count("tasks", distinct=True)))

    context = {
        "user_tasks": user_tasks,
        "total_tasks": total_tasks,
        "in_progress": in_progress,
        "missed_tasks": missed,
        "user_teams": teams
    }
    return render(request, "task_manage/dashboard.html", context)