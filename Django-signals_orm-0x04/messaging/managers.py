from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager that exposes helpers for fetching unread messages
    for a given user, optimized with `.only()` to load just the fields
    needed for an inbox view.
    """

    def unread_for_user(self, user):
        """
        Return unread messages for the given user.
        """
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "content", "sender", "timestamp", "parent_message")
            .select_related("sender")
        )

    # Backwards-compatible alias
    def for_user(self, user):
        return self.unread_for_user(user)


