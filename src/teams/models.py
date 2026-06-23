from django.db import models
from accounts.models import CustomUser


class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # не можна змінити

    def __str__(self):
        return f"{self.name} created at {self.created_at} by {self.owner}"


class TeamMember(models.Model):
    ROLES = [('owner', 'Власник'), ('admin', 'Адміністратор'), ('member', 'Учасник')]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user} ({self.role}) - {self.team}"
