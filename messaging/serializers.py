from rest_framework import serializers

from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Message, ChatThread



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

    def create(self, validated):
        req = self.context["request"]
        thread = ChatThread.get_pair(req.user.id, validated["receiver"].id)
        return Message.objects.create(
            sender=req.user,
            receiver=validated["receiver"],
            content=validated["content"],
            thread=thread,
        )



class ThreadSerializer(serializers.ModelSerializer):
    other = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatThread
        fields = ("id", "other", "updated_at", "last_message")

    def get_other(self, obj):
        u = self.context["request"].user
        other = obj.user_b if obj.user_a_id == u.id else obj.user_a
        return {"id": other.id, "email": other.email}

    def get_last_message(self, obj):
        m = obj.messages.order_by("-id").first()
        if not m:
            return None
        return {"id": m.id, "content": m.content, "created_at": m.created_at}



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
