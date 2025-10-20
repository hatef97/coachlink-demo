from django.db import models
from django.conf import settings



class Session(models.Model):
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions_as_coach")
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions_as_client")
    start_time = models.DateTimeField()
    duration_min = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=16, default="scheduled")  # scheduled|cancelled|done
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("start_time",)
