from rest_framework import generics, permissions

from django_filters.rest_framework import DjangoFilterBackend

from .models import Profile
from .serializers import MyProfileSerializer, PublicCoachSerializer



class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile



class CoachListView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_coach=True)
    serializer_class = PublicCoachSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["field", "experience", "city"]
