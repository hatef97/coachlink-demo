from django.db import models
from django.conf import settings



class ChatThread(models.Model):
    user_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads_a")
    user_b = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads_b")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_a", "user_b"], name="uniq_chat_pair")
        ]

    @staticmethod
    def get_pair(u1_id, u2_id):
        a, b = sorted([u1_id, u2_id])
        obj, _ = ChatThread.objects.get_or_create(user_a_id=a, user_b_id=b)
        return obj



class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name="messages", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:30]}"
