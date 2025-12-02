"""Signal handlers for the messaging app."""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save, pre_save
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


User = get_user_model()


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs) -> None:
    """
    After a User is deleted, clean up all related messaging data.

    This includes messages (as sender or receiver), notifications, and
    any message histories tied to those messages.
    """
    # Delete messages where the user is sender or receiver
    messages_qs = Message.objects.filter(sender=instance) | Message.objects.filter(
        receiver=instance
    )
    message_ids = list(messages_qs.values_list("id", flat=True))

    messages_qs.delete()

    # Delete notifications explicitly associated with the user
    Notification.objects.filter(user=instance).delete()

    # Delete any remaining histories tied to those messages (safety, in case
    # database constraints are different)
    if message_ids:
        MessageHistory.objects.filter(message_id__in=message_ids).delete()

