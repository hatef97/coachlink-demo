from django.contrib import admin

from .models import Coach, SessionRequest



@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ("id","user","title","price_per_session","currency","session_duration_min","is_verified","updated_at")
    search_fields = ("user__email","title","certifications","specializations")
    list_filter = ("is_verified",)
    raw_id_fields = ("user",)



@admin.register(SessionRequest)
class SessionRequestAdmin(admin.ModelAdmin):
    list_display = ("id","requester","coach","status","preferred_time","created_at")
    list_filter = ("status","created_at")
    search_fields = ("requester__email","coach__email","message")
    raw_id_fields = ("requester","coach")
