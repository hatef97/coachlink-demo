from rest_framework import generics, permissions
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Coach, SessionRequest
from .serializers import (
    CoachMeSerializer, PublicCoachDetailSerializer,
    SessionRequestCreateSerializer, SessionRequestSerializer, SessionRequestStatusSerializer
)
from .permissions import IsCoach



User = get_user_model()


class BecomeCoachView(generics.CreateAPIView):
    """
    POST: create your Coach profile (once).
    """
    serializer_class = CoachMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, "coach"):
            return Response({"detail": "You are already a coach."}, status=400)
        coach = Coach.objects.create(user=request.user)
        ser = self.get_serializer(instance=coach, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        # also flip profile flag if you use profiles.is_coach
        if hasattr(request.user, "profile") and not request.user.profile.is_coach:
            request.user.profile.is_coach = True
            request.user.profile.save(update_fields=["is_coach"])
        return Response(ser.data, status=201)



class MyCoachProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CoachMeSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoach]

    def get_object(self):
        return self.request.user.coach



class PublicCoachDetailView(generics.RetrieveAPIView):
    """
    GET /api/coaches/<user_id>/detail/
    """
    queryset = Coach.objects.select_related("user")
    serializer_class = PublicCoachDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "user_id"



class SessionRequestCreateView(generics.CreateAPIView):
    serializer_class = SessionRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]



class MyIncomingSessionRequestsView(generics.ListAPIView):
    """
    Coach inbox for session requests
    """
    serializer_class = SessionRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoach]

    def get_queryset(self):
        return SessionRequest.objects.filter(coach=self.request.user).select_related("coach","requester")



class MyOutgoingSessionRequestsView(generics.ListAPIView):
    """
    Requests I (as a user) sent to coaches
    """
    serializer_class = SessionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SessionRequest.objects.filter(requester=self.request.user).select_related("coach","requester")



class SessionRequestStatusView(generics.UpdateAPIView):
    """
    Coach updates status (accepted/declined)
    """
    serializer_class = SessionRequestStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoach]
    queryset = SessionRequest.objects.all()

    def get_object(self):
        obj = get_object_or_404(SessionRequest, pk=self.kwargs["pk"])
        if obj.coach_id != self.request.user.id:
            # only the targeted coach can change status
            self.permission_denied(self.request, message="Not your request.")
        return obj
