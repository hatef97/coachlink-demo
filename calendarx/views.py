from rest_framework import generics, permissions

from django.db.models import Q

from .models import Session
from .serializers import SessionSerializer



class MySessionsView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return Session.objects.filter(Q(coach=u) | Q(client=u)).order_by("start_time")

    def perform_create(self, serializer):
        # allow creating manually; must include both coach and client as current user or partner
        u = self.request.user
        data = serializer.validated_data
        # minimal safety: user must be coach or client
        if not (data.get("coach") == u or data.get("client") == u):
            self.permission_denied(self.request, message="You must be a participant.")
        serializer.save()
