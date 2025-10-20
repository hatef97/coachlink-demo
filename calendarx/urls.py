from django.urls import path

from .views import MySessionsView



urlpatterns = [
    path("calendar/sessions/", MySessionsView.as_view(), name="my_sessions"),
]
