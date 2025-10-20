from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



User = get_user_model()


class EmailOrPhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    identifier = serializers.CharField(label="Email or phone number")
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop(self.username_field, None)

    def validate(self, attrs):
        identifier = (attrs.get("identifier") or "").strip()
        password = attrs.get("password") or ""

        user = (User.objects.filter(email__iexact=identifier).first()
                or User.objects.filter(phone=identifier).first())

        if not user or not user.check_password(password) or not user.is_active:
            raise AuthenticationFailed("Invalid credentials")

        self.user = user
        return super().validate({"email": user.email, "password": password})


class EmailOrPhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrPhoneTokenObtainPairSerializer
