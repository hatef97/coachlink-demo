from rest_framework import generics, permissions, mixins
from rest_framework.response import Response

from django.db.models import Q

from .models import Message
from .serializers import (
    MessageCreateSerializer, MessageSerializer, MarkReadSerializer
)
from .permissions import IsParticipant



class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]



class InboxListView(generics.ListAPIView):
    """
    All conversations involving current user (both sent and received).
    Optional query params:
      - with=<user_id>  → thread with a specific user
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        qs = Message.objects.filter(Q(sender=u) | Q(receiver=u))
        other_id = self.request.query_params.get("with")
        if other_id:
            qs = qs.filter(Q(sender_id=other_id, receiver=u) | Q(receiver_id=other_id, sender=u))
        return qs.select_related("sender", "receiver")



class MessageDetailView(mixins.UpdateModelMixin,
                        generics.RetrieveAPIView):
    """
    GET: retrieve a single message (only if participant)
    PATCH: { "read": true|false } mark read/unread
    """
    queryset = Message.objects.all().select_related("sender", "receiver")
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return MarkReadSerializer
        return MessageSerializer

    def patch(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_object())
        return self.partial_update(request, *args, **kwargs)
