from django.db import models

from accounts.models import CustomUser
from teams.models import Team

class Category(models.Model):
    name = models.CharField(max_length=64)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.team}"


class Task(models.Model):
    PRIORITIES = [('high', 'Високий'), ('medium', 'Середній'), ('low', 'Низький')]
    STATUSES = [('to_do', 'Необхідно виконати'), ('in_progress', 'Виконується'), ('done', 'Готовий')]

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1000, blank=True)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    status = models.CharField(max_length=32, choices=STATUSES)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(CustomUser, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="assigned_tasks")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_tasks")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return f"Title: {self.title}, deadline: {self.deadline}, assigned_to: {self.assigned_to}"
