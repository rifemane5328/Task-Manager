from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    ordering = ['first_name', 'last_name']
