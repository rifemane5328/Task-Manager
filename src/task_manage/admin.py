from django.contrib import admin
from .models import Task, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'deadline', 'priority', 'status',
                    'category', 'assigned_to', 'created_by', 'team_name']
    list_display_links = ['description']
    list_filter = ['deadline', 'priority', 'status', 'category',
                    'assigned_to', 'created_by', 'team__name']
    list_editable = ['title', 'priority', 'status', 'category']
    ordering = ['title', 'deadline', 'created_by']

    @admin.display(description='Team')
    def team_name(self, obj):
        return obj.team.name if obj.team else '-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'team_name']
    list_filter = ['team__name']
    ordering = ['name']

    @admin.display(description='Team')
    def team_name(self, obj):
        return obj.team.name if obj.team else '-'
