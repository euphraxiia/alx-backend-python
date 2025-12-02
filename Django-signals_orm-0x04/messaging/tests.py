from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Message, MessageHistory, Notification


class MessageSignalTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.sender = User.objects.create_user(
            username="sender", email="sender@example.com", password="pass1234"
        )
        self.receiver = User.objects.create_user(
            username="receiver", email="receiver@example.com", password="pass1234"
        )

    def test_notification_created_on_new_message(self) -> None:
        """A Notification is automatically created when a new Message is saved."""
        message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hello there!"
        )

        notifications = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notifications.count(), 1)

    def test_no_duplicate_notification_on_update(self) -> None:
        """Updating an existing Message must not create an extra Notification."""
        message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Initial"
        )
        # One notification for the create
        self.assertEqual(
            Notification.objects.filter(user=self.receiver, message=message).count(),
            1,
        )

        # Update message content
        message.content = "Updated"
        message.save()

        # Still only one notification
        self.assertEqual(
            Notification.objects.filter(user=self.receiver, message=message).count(),
            1,
        )

    def test_message_history_created_on_edit(self) -> None:
        """Editing a message logs the old content in MessageHistory and sets edited flag."""
        message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Original content"
        )
        self.assertFalse(message.edited)

        # Edit the message
        message.content = "Edited content"
        message.save()

        # Refresh from DB to get updated edited flag
        message.refresh_from_db()
        self.assertTrue(message.edited)

        history_entries = MessageHistory.objects.filter(message=message)
        self.assertEqual(history_entries.count(), 1)
        self.assertEqual(history_entries.first().old_content, "Original content")

