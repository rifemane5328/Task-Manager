from django.shortcuts import render
from django.db.models import Count, Subquery, OuterRef, Q
from datetime import date

from .models import Team, TeamMember
from task_manage.models import Task

def teams_view(request):
    teams = Team.objects.filter(members__user=request.user).annotate(member_count=Count('members', distinct=True)
        ).annotate(task_count=Count('tasks', distinct=True)).annotate(active_tasks_count=Count(
        'tasks', filter=~Q(tasks__status='done'), distinct=True)).annotate(missed_tasks_count=Count(
        'tasks', filter=Q(tasks__deadline__lt=date.today()) & ~Q(tasks__status='done'), distinct=True)
        ).annotate(user_role=Subquery(
            TeamMember.objects.filter(team=OuterRef('pk'), user=request.user).values('role')[:1]))

    context = {
        "teams": teams
    }

    return render(request, "teams/teams.html", context)


def team_detail_view(request):
    ...
