from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



User = get_user_model()


class EmailOrPhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    # client sends: { "identifier": "<email or phone>", "password": "..." }
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        identifier = (attrs.get("identifier") or "").strip()
        password = attrs.get("password") or ""

        # Try email (case-insensitive), then phone (exact)
        user = (User.objects.filter(email__iexact=identifier).first()
                or User.objects.filter(phone=identifier).first())

        if not user or not user.check_password(password) or not user.is_active:
            raise AuthenticationFailed("Invalid credentials")

        self.user = user
        data = super().validate({"email": user.email, "password": password})
        return data


class EmailOrPhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrPhoneTokenObtainPairSerializer
