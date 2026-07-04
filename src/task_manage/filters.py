import django_filters
from django import forms

from .models import Task, Category
from teams.models import Team


def get_user_categories(request):
    if request is None:
        return Category.objects.none()
    return Category.objects.filter(tasks__assigned_to=request.user).distinct()

class TaskFilter(django_filters.FilterSet):
    PRIORITIES = [('high', 'Високий'), ('medium', 'Середній'), ('low', 'Низький')]
    STATUSES = [('to_do', 'Необхідно виконати'), ('in_progress', 'Виконується'), ('done', 'Готовий')]

    title = django_filters.CharFilter(method='by_name_filter')
    deadline_after = django_filters.DateFilter(field_name='deadline', lookup_expr='gte')
    deadline_before = django_filters.DateFilter(field_name='deadline', lookup_expr='lte')
    priority = django_filters.ChoiceFilter(choices=PRIORITIES)
    status = django_filters.ChoiceFilter(choices=STATUSES)
    category = django_filters.ModelChoiceFilter(queryset=get_user_categories, 
        empty_label="Усі категорії", widget=forms.Select(attrs={"class": "form-select mb-2"}))

    class Meta:
        model = Task
        fields = ['deadline', 'priority', 'status', 'category']

    def by_name_filter(self, queryset, title, value):
        if value.strip():
            return queryset.filter(title__icontains=value)
        return queryset