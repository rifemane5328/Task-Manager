from django.contrib import admin
from .models import Team, TeamMember

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']
    list_display_links = ['owner']
    list_filter = ['owner']
    list_editable = ['name']
    ordering = ['name', 'created_at']


@admin.register(TeamMember)
class TeamMember(admin.ModelAdmin):
    list_display = ['user', 'team_name', 'role']
    list_filter = ['user', 'team__name', 'role']
    ordering = ['user', 'team']

    @admin.display(description='Team')
    def team_name(self, obj):
        return obj.team.name if obj.team else '-'