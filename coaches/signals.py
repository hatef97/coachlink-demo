from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from .models import SessionRequest



@receiver(post_save, sender=SessionRequest)
def notify_on_session_request(sender, instance, created, **kwargs):
    Notification = apps.get_model("notifications", "Notification")
    if created:
        Notification.objects.create(
            user=instance.coach, kind="request_new",
            payload={"request_id": instance.id, "from": instance.requester_id}
        )
    else:
        # status changed → notify requester
        Notification.objects.create(
            user=instance.requester, kind="request_status",
            payload={"request_id": instance.id, "status": instance.status}
        )
