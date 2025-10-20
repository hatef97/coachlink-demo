from rest_framework import serializers

from .models import Session



class SessionSerializer(serializers.ModelSerializer):
    coach = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ("id","coach","client","start_time","duration_min","status","note")

    def get_coach(self, obj): return {"id": obj.coach_id, "email": obj.coach.email}
    def get_client(self, obj): return {"id": obj.client_id, "email": obj.client.email}
