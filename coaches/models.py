from django.db import models
from django.conf import settings



class Coach(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coach")
    # professional profile
    title = models.CharField(max_length=120, blank=True)                 # e.g., Strength Coach
    bio = models.TextField(blank=True)                                   # description
    certifications = models.TextField(blank=True)                        # plain text list (minimal)
    specializations = models.JSONField(default=list, blank=True)         # ["fitness","nutrition"]
    price_per_session = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, default="USD")
    session_duration_min = models.PositiveIntegerField(default=60)
    is_verified = models.BooleanField(default=False)                      # for admin use
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Coach<{self.user.email}>"



class SessionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="session_requests_made")
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="session_requests_received")
    message = models.TextField(blank=True)
    preferred_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.requester} → {self.coach} ({self.status})"
