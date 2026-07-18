import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Subquery, OuterRef, Q
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date

from .models import Team, TeamMember
from task_manage.models import Task, Category
from task_manage.filters import TaskFilter
from task_manage.forms import TaskEditingForm, TaskMemberEditingForm


@login_required
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


def get_user_role(team, user):
    membership = team.members.filter(user=user).first()
    return membership.role if membership else None

def get_team_or_403(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    user_role = get_user_role(team, request.user)
    if user_role is None:
        return None, None
    return team, user_role


@login_required
def team_tasks_view(request, team_id):
    team, user_role = get_team_or_403(request, team_id)
    if team is None:
        return HttpResponseForbidden
    categories = team.categories.all()

    team_members = {
        team.id: [
            {"id": m.user.id, "name": m.user.full_name}
            for m in team.members.all()
        ]
    }

    task_filter = TaskFilter(
        request.GET,
        queryset=team.tasks.select_related('category', 'assigned_to', 'created_by'),
        request=request, team_id=team_id)
    
    paginator = Paginator(task_filter.qs, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "team": team,
        "user_role": user_role,
        "filter": task_filter,
        "tasks": task_filter.qs,
        "page_obj": page_obj,
        "categories": categories,
        "team_members_json": team_members
        }
    return render(request, "teams/team_tasks.html", context)


@login_required
def team_edit_task_view(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    team, user_role = get_team_or_403(request, team_id=task.team.id)
    if team is None:
        return HttpResponseForbidden

    can_edit = (user_role in ('owner', 'admin')
    or task.assigned_to == request.user
    or task.created_by == request.user
    )
    if not can_edit:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        if user_role in ('owner', 'admin'):
            form = TaskEditingForm(request.POST, instance=task)
        elif user_role == 'member':
            form = TaskMemberEditingForm(request.POST, instance=task)
        else:
            return HttpResponseForbidden()
        if form.is_valid():
            form.save()
            messages.success(request, "Завдання успішно змінено.")
        else:
            messages.error(request, "Не вдалося зберегти зміни." \
            "\nБудь ласка, перевірте правильність вхідних даних.")
        return redirect("teams:team_detail", team_id=team.id)
        
    return redirect("teams:team_detail", team_id=team.id)


@login_required
def team_members_view(request, team_id):
    team, user_role = get_team_or_403(request, team_id)
    if team is None:
        return HttpResponseForbidden
    context = {
        "team": team,
        "user_role": user_role
        }
    return render(request, "teams/team_members.html", context)


@login_required
def team_settings_view(request, team_id):
    team, user_role = get_team_or_403(request, team_id)
    if team is None:
        return HttpResponseForbidden
    if user_role != 'owner':
        return HttpResponseForbidden()
    context = {
        "team": team,
        "user_role": user_role
        }
    return render(request, "teams/team_settings.html", context)