from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User



@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("email",)
    list_display = ("id", "email", "is_active", "is_staff")
    search_fields = ("email", "phone")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("phone",)}),
        ("Permissions", {"fields": ("is_active","is_staff","is_superuser","groups","user_permissions")}),
        ("Important dates", {"fields": ("last_login","date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions")
