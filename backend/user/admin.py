from django.contrib import admin
from .models import User, Role
# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")
    ordering = ("username",)