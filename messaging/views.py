from rest_framework import generics, permissions, mixins
from rest_framework.response import Response

from django.db.models import Q

from .models import Message, ChatThread
from .serializers import (
    MessageCreateSerializer, MessageSerializer, MarkReadSerializer, ThreadSerializer
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



class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return ChatThread.objects.filter(models.Q(user_a=u) | models.Q(user_b=u)).prefetch_related("messages","user_a","user_b").order_by("-updated_at")



class ThreadMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        thread_id = self.kwargs["thread_id"]
        thread = ChatThread.objects.get(pk=thread_id)
        if u.id not in (thread.user_a_id, thread.user_b_id):
            self.permission_denied(self.request, message="Not your thread.")
        return Message.objects.filter(thread=thread).select_related("sender","receiver").order_by("-created_at")
