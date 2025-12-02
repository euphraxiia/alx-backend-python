from django.conf import settings
from django.db import models

from .managers import UnreadMessagesManager


class MessageQuerySet(models.QuerySet):
    """
    Custom queryset with helpers for fetching threaded conversations efficiently.
    """

    def with_related(self):
        """
        Optimize queries by selecting related users and parent message,
        and prefetching replies.
        """
        return (
            self.select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
        )

    def thread_for(self, root_message: "Message") -> list["Message"]:
        """
        Return all messages belonging to the thread rooted at `root_message`,
        ordered by timestamp.
        """
        # Fetch all messages that are the root or have an ancestor equal to root.
        # For simplicity in this exercise, we pull all messages for the
        # participants and build the tree in Python.
        qs = (
            self.filter(
                models.Q(sender=root_message.sender, receiver=root_message.receiver)
                | models.Q(sender=root_message.receiver, receiver=root_message.sender)
            )
            .with_related()
            .order_by("timestamp")
        )
        return list(qs)


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
    # Mark whether the message has been read by the receiver
    read = models.BooleanField(default=False)
    # Track whether the message has ever been edited after creation
    edited = models.BooleanField(default=False)
    # Optional reference to the user who performed the last edit
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages",
    )

    # Self-referential foreign key to support threaded replies
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    objects = MessageQuerySet.as_manager()
    unread = UnreadMessagesManager()

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    def get_thread(self) -> list["Message"]:
        """
        Return the full conversation thread for this message in a threaded structure.

        The result is a flat list ordered by timestamp, but replies can be
        grouped on the client side using the `parent_message` relation.
        """
        return Message.objects.thread_for(self)


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


