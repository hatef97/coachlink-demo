from django.db import models
from django.conf import settings



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # personal
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    goal = models.CharField(max_length=255, blank=True)
    activity_type = models.CharField(max_length=255, blank=True)
    # discovery/filter fields
    field = models.CharField(max_length=100, blank=True)         
    experience = models.PositiveIntegerField(default=0)            
    city = models.CharField(max_length=100, blank=True)
    is_coach = models.BooleanField(default=False)                  

    def __str__(self):
        return f"{self.user.email}"
