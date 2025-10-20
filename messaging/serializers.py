from rest_framework import serializers

from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Message



User = get_user_model()


class MessageCreateSerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ("receiver", "content")

    def validate(self, attrs):
        req = self.context["request"]
        if attrs["receiver"] == req.user:
            raise serializers.ValidationError("You cannot message yourself.")
        return attrs

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)



class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("id", "sender", "receiver", "content", "created_at", "read_at", "is_read")

    def get_sender(self, obj):  # minimal public fields
        return {"id": obj.sender.id, "email": obj.sender.email}

    def get_receiver(self, obj):
        return {"id": obj.receiver.id, "email": obj.receiver.email}

    def get_is_read(self, obj):
        return obj.read_at is not None



class MarkReadSerializer(serializers.Serializer):
    read = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.read_at = timezone.now() if validated_data["read"] else None
        instance.save(update_fields=["read_at"])
        return instance
