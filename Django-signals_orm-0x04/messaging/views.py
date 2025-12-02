from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import Message


@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    """
    View that allows the currently authenticated user to delete their account.

    This will trigger post_delete signals on the User model so that all
    related messages, notifications, and message histories are cleaned up.
    """
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    user = request.user

    # Log the user out before deleting the account
    logout(request)

    User = get_user_model()
    # Refetch from DB to avoid issues with custom User managers, then delete
    try:
        db_user = User.objects.get(pk=user.pk)
    except User.DoesNotExist:
        return JsonResponse({"detail": "User not found."}, status=404)

    db_user.delete()

    return JsonResponse({"detail": "Account deleted successfully."}, status=200)


@login_required
def threaded_conversation(request: HttpRequest, receiver_id: int) -> HttpResponse:
    """
    Return a threaded view of all messages between the current user and `receiver`.

    Uses select_related and prefetch_related to efficiently load messages
    and their replies, then builds a recursive tree structure suitable for
    display in the UI.
    """
    User = get_user_model()
    try:
        receiver = User.objects.get(pk=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({"detail": "Receiver not found."}, status=404)

    # Base queryset: all messages between the two users
    qs = (
        Message.objects.filter(
            Q(sender=request.user, receiver=receiver)
            | Q(sender=receiver, receiver=request.user)
        )
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies")
        .order_by("timestamp")
    )

    # Build an in-memory tree of messages -> replies
    messages_by_id = {m.id: m for m in qs}
    children_map: dict[int | None, list[Message]] = {}
    for message in qs:
        parent_id = message.parent_message_id
        children_map.setdefault(parent_id, []).append(message)

    def build_node(msg: Message) -> dict:
        return {
            "id": msg.id,
            "content": msg.content,
            "sender": str(msg.sender),
            "receiver": str(msg.receiver),
            "timestamp": msg.timestamp.isoformat(),
            "edited": msg.edited,
            "replies": [
                build_node(child) for child in children_map.get(msg.id, [])
            ],
        }

    # Root messages have no parent_message
    root_messages = children_map.get(None, [])
    thread = [build_node(m) for m in root_messages]

    return JsonResponse(thread, safe=False)


