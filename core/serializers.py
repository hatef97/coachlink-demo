from rest_framework import serializers

from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email","phone")



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8,
                                     style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, label="Password (again)",
                                      style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("email", "phone", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            phone=validated_data.get("phone"),
        )
        