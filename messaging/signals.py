from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from .models import Message



@receiver(post_save, sender=Message)
def notify_on_message(sender, instance, created, **kwargs):
    if not created:
        return
    Notification = apps.get_model("notifications", "Notification")
    Notification.objects.create(
        user=instance.receiver,
        kind="message_new",
        payload={"message_id": instance.id, "from": instance.sender_id, "thread_id": instance.thread_id},
    )
