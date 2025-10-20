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



@receiver(post_save, sender=SessionRequest)
def create_session_on_accept(sender, instance, created, **kwargs):
    if created:
        return
    if instance.status == SessionRequest.Status.ACCEPTED and instance.preferred_time:
        Session = apps.get_model("calendarx", "Session")
        # avoid duplicates
        exists = Session.objects.filter(coach=instance.coach, client=instance.requester, start_time=instance.preferred_time).exists()
        if not exists:
            Session.objects.create(
                coach=instance.coach,
                client=instance.requester,
                start_time=instance.preferred_time,
                duration_min=60,
                note="Auto from accepted request",
            )
            