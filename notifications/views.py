from rest_framework import generics, permissions

from .models import Notification
from .serializers import NotificationSerializer



class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)



class NotificationUnreadCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        from rest_framework.response import Response
        return Response({"unread": count})



class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    http_method_names = ["patch"]

    def perform_update(self, serializer):
        # only owner can mark read
        if serializer.instance.user_id != self.request.user.id:
            self.permission_denied(self.request, message="Not your notification.")
        serializer.save(is_read=True)
