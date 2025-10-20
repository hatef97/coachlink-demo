from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Coach, SessionRequest



User = get_user_model()


class CoachMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ("title","bio","certifications","specializations","price_per_session","currency","session_duration_min")



class PublicCoachDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    class Meta:
        model = Coach
        fields = ("id","email","title","bio","certifications","specializations","price_per_session","currency","session_duration_min")



class SessionRequestCreateSerializer(serializers.ModelSerializer):
    coach_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SessionRequest
        fields = ("coach_id","message","preferred_time")

    def validate(self, attrs):
        req = self.context["request"]
        coach_id = attrs.get("coach_id")
        try:
            coach_user = User.objects.get(id=coach_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"coach_id": "Coach user not found."})
        # must be a coach
        if not hasattr(coach_user, "coach"):
            raise serializers.ValidationError({"coach_id": "Target user is not a coach."})
        if coach_user.id == req.user.id:
            raise serializers.ValidationError("You cannot request a session with yourself.")
        attrs["coach_user"] = coach_user
        return attrs

    def create(self, validated_data):
        req = self.context["request"]
        coach_user = validated_data.pop("coach_user")
        return SessionRequest.objects.create(
            requester=req.user,
            coach=coach_user,
            **validated_data
        )



class SessionRequestSerializer(serializers.ModelSerializer):
    requester = serializers.SerializerMethodField()
    coach = serializers.SerializerMethodField()
    class Meta:
        model = SessionRequest
        fields = ("id","requester","coach","message","preferred_time","status","created_at")

    def get_requester(self, obj):
        return {"id": obj.requester.id, "email": obj.requester.email}

    def get_coach(self, obj):
        return {"id": obj.coach.id, "email": obj.coach.email}



class SessionRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRequest
        fields = ("status",)
