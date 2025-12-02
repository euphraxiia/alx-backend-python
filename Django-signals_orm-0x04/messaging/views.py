from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse


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



