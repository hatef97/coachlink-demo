from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("core.urls")),
    path("api/", include("profiles.urls")),
    path("api/", include("messaging.urls")),
    path("api/", include("coaches.urls")),
    path("api/", include("notifications.urls")),
    path("api/", include("calendarx.urls")),
]
