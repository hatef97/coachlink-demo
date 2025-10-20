from django.contrib import admin

from .models import Message



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "short", "created_at", "read_at")
    list_filter = ("created_at",)
    search_fields = ("sender__email", "receiver__email", "content")

    def short(self, obj):
        return (obj.content[:60] + "…") if len(obj.content) > 60 else obj.content
