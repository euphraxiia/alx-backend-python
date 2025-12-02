from django.conf import settings
from django.db import models


class Message(models.Model):
    """
    Message model representing a chat message sent from one user to another.
    """

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Track whether the message has ever been edited after creation
    edited = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"


class MessageHistory(models.Model):
    """
    Stores previous versions of a Message's content before it was edited.
    """

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="history",
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"History for message {self.message_id} at {self.edited_at}"


class Notification(models.Model):
    """
    Notification created for a user when they receive a new Message.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Notification for {self.user} about message {self.message_id}"


