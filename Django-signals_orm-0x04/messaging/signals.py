"""Signal handlers for the messaging app."""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Message, MessageHistory, Notification


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


@receiver(pre_save, sender=Message)
def log_message_edit(
    sender, instance: Message, **kwargs
) -> None:
    """
    Before a Message is updated, store the previous content in MessageHistory.
    """
    if instance.pk is None:
        # New message being created; nothing to log
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If the content is changing, record the old content and mark as edited
    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content,
        )
        instance.edited = True

