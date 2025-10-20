from django.db import models
from django.conf import settings



class Notification(models.Model):
    class Kind(models.TextChoices):
        MESSAGE_NEW = "message_new", "New message"
        REQUEST_NEW = "request_new", "New session request"
        REQUEST_STATUS = "request_status", "Session request status"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    kind = models.CharField(max_length=32, choices=Kind.choices)
    payload = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
