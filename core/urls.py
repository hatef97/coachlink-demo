from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, MeView
from .auth import EmailOrPhoneTokenObtainPairView



urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", EmailOrPhoneTokenObtainPairView.as_view(), name="login_eop"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
]
