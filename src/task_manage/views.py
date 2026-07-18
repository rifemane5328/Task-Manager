import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Subquery, OuterRef
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date

from .models import Task, Category
from teams.models import Team, TeamMember
from accounts.models import CustomUser
from .filters import TaskFilter
from. forms import TaskEditingForm, TaskMemberEditingForm


@login_required
def profile_view(request):
    user = request.user
    context = {
        "user": user
    }
    return render(request, "task_manage/profile.html", context)

@login_required
def dashboard_view(request):
    base_tasks = Task.objects.filter(assigned_to=request.user)

    total_tasks = base_tasks.count()
    user_tasks = base_tasks.order_by("deadline")[:5]
    in_progress = base_tasks.filter(status="in_progress").count()
    missed = Task.objects.filter(assigned_to=request.user, deadline__lt=date.today()).exclude(status="done").count()

    teams = (Team.objects.filter(members__user=request.user).annotate(
        member_count=Subquery(TeamMember.objects.filter(team=OuterRef('pk')).values('team').annotate(count=Count('id')).values('count')[:1]
    )).annotate(
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
    # Створюємо ролі для кожного учасника поточного користувача
    role_subquery = Subquery(TeamMember.objects.filter(
        user=request.user, team=OuterRef('team')
        ).values('role')[:1])
    
    tasks = Task.objects.filter(assigned_to=request.user).order_by("title").select_related(
        'category', 'assigned_to', 'team').annotate(user_role=role_subquery)

    user_teams = Team.objects.filter(members__user=request.user).prefetch_related("members__user")

    # Створюємо словник з id команд та їх учасниками
    team_members_dict = {}
    for team in user_teams:
        team_members_dict[team.id] = [
            {'id': member.user.id, 'name': member.user.full_name}
            for member in team.members.all()
        ]

    categories = Category.objects.filter(team__in=user_teams)
    task_filter = TaskFilter(request.GET, queryset=tasks, request=request)

    paginator = Paginator(task_filter.qs, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "filter": task_filter,
        "team_members_json": team_members_dict,
        "categories": categories,
        "page_obj": page_obj
    }

    return render(request, "task_manage/my_tasks.html", context)


@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if request.method == "POST":
        member = TeamMember.objects.filter(user=request.user, team=task.team).first()
        if not member:
            messages.error(request, "У вас не має доступу до цього завдання.")
            return redirect("task_manage:my_tasks")
        user_role = member.role

        if user_role in ('owner', 'admin'):
            form = TaskEditingForm(request.POST, instance=task)
        elif user_role == "member":
            form = TaskMemberEditingForm(request.POST, instance=task)

        if form.is_valid():
            new_assigned_to = form.cleaned_data.get('assigned_to')
            if new_assigned_to:

                # Перевіряємо чи можна призначити завдання цьому користувачу
                is_valid_member = TeamMember.objects.filter(
                    user=new_assigned_to,
                    team=task.team 
                ).exists()
                if not is_valid_member:
                    messages.error(request, "Цей користувач не є членом команди поточного завдання," \
                    "\nтому завдання не може бути призначене йому.")
                    return redirect("task_manage:my_tasks")
            form.save()
            messages.success(request, "Завдання успішно змінено.")
        else:
            messages.error(request, "Не вдалося зберегти зміни." \
            "\nБудь ласка, перевірте правильність вхідних даних.")
        return redirect("task_manage:my_tasks")

    return redirect("task_manage:my_tasks")