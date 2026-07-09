from django import forms
from .models import Task


# Для власника та адмінів
class TaskEditingForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'priority', 'status', 'category', 'assigned_to']


# Для учасника
class TaskMemberEditingForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'status']
