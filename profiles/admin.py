from django.contrib import admin
from django.utils.html import format_html

from .models import Profile



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_email", "is_coach", "field", "experience", "city", "photo_tag",
    )
    list_filter = ("is_coach", "field", "city", "experience")
    search_fields = ("user__email", "user__phone", "field", "city")
    ordering = ("-id",)
    raw_id_fields = ("user",)
    readonly_fields = ("photo_preview",)
    fieldsets = (
        ("Owner", {"fields": ("user",)}),
        ("Profile", {"fields": ("photo", "photo_preview", "goal", "activity_type")}),
        ("Discovery", {"fields": ("is_coach", "field", "experience", "city")}),
    )

    def user_email(self, obj):
        return getattr(obj.user, "email", "")
    user_email.short_description = "Email"

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:38px;border-radius:6px;" />', obj.photo.url)
        return "—"
    photo_tag.short_description = "Photo"

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', obj.photo.url)
        return "No image"
    photo_preview.short_description = "Preview"
