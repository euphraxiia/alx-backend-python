"""Signal handlers for the messaging app."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification_on_message(
    sender, instance: Message, created: bool, **kwargs
) -> None:
    """
    Create a Notification whenever a new Message is created.
    """
    if not created:
        return

    Notification.objects.create(
        user=instance.receiver,
        message=instance,
    )


