from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительно",
            {"fields": ("phone", "friends")},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Дополнительно",
            {"fields": ("email", "phone")},
        ),
    )
