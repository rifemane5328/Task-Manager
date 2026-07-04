from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Subquery, OuterRef
from django.core.paginator import Paginator
from datetime import date

from .models import Task
from teams.models import Team, TeamMember
from .filters import TaskFilter


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

@login_required
def my_tasks_view(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    task_filter = TaskFilter(request.GET, queryset=tasks, request=request)

    paginator = Paginator(task_filter.qs, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "filter": task_filter,
        "tasks": task_filter.qs,
        "page_obj": page_obj
    }

    return render(request, "task_manage/my_tasks.html", context)