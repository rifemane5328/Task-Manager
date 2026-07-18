import django_filters
from django_filters import CharFilter, DateFilter, ChoiceFilter, ModelChoiceFilter
from django import forms

from .models import Task, Category
from accounts.models import CustomUser
from teams.models import Team


def get_team_users(request, team_id):
    if not request:
        return CustomUser.objects.none()
    team = Team.objects.get(id=team_id)
    return CustomUser.objects.filter(team_memberships__team=team)

def get_user_categories(request):
    if request is None:
        return Category.objects.none()
    return Category.objects.filter(tasks__assigned_to=request.user).distinct()

def get_team_categories(request, team_id):
    if request is None:
        return Category.objects.none()
    return Category.objects.filter(team=Team.objects.get(id=team_id))

class TaskFilter(django_filters.FilterSet):
    # Filters user's tasks
    PRIORITIES = [('high', 'Високий'), ('medium', 'Середній'), ('low', 'Низький')]
    STATUSES = [('to_do', 'Необхідно виконати'), ('in_progress', 'Виконується'), ('done', 'Готовий')]

    title = CharFilter(method='by_name_filter')
    deadline_after = DateFilter(field_name='deadline', lookup_expr='gte')
    deadline_before = DateFilter(field_name='deadline', lookup_expr='lte')
    priority = ChoiceFilter(choices=PRIORITIES)
    status = ChoiceFilter(choices=STATUSES)
    category = ModelChoiceFilter(queryset=Category.objects.none(), # початкове значення
        empty_label="Усі категорії", widget=forms.Select(attrs={"class": "form-select mb-2"}))
    assigned_to = ModelChoiceFilter(queryset=get_team_users, 
        empty_label="Усі призначення", widget=forms.Select(attrs={"class": "form-select mb-2"}))

    class Meta:
        model = Task
        fields = ['title', 'deadline', 'priority', 'status', 'category', 'assigned_to']

    def by_name_filter(self, queryset, title, value):
        if value:
            value = value.strip()
            return queryset.filter(title__icontains=value)
        return queryset
    
    # Дістаємо team_id з kwargs для використання у фільтрі    
    def __init__(self, *args, **kwargs):
        self.team_id = kwargs.pop('team_id', None)
        super().__init__(*args, **kwargs)
        if self.team_id:
            self.filters['assigned_to'].queryset = get_team_users(self.request, self.team_id)
            self.filters['category'].queryset = get_team_categories(self.request, self.team_id)
        else:
            del self.filters['assigned_to']
            self.filters['category'].queryset = get_user_categories(self.request)