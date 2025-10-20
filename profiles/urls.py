from django.urls import path

from .views import MyProfileView, CoachListView



urlpatterns = [
    path("profile/me/", MyProfileView.as_view(), name="my_profile"),
    path("coaches/", CoachListView.as_view(), name="coach_list"),
]
