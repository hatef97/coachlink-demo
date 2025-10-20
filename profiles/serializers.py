from rest_framework import serializers

from .models import Profile



class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "photo", "goal", "activity_type",
            "field", "experience", "city", "is_coach",
        )



class PublicCoachSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "email", "photo", "field", "experience", "city")
