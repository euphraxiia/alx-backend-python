from datetime import datetime
from pathlib import Path

from django.conf import settings


LOG_FILE_PATH = Path(settings.BASE_DIR) / "requests.log"


class RequestLoggingMiddleware:
    """
    Middleware that logs every incoming request with a timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        LOG_FILE_PATH.touch(exist_ok=True)

    def __call__(self, request):
        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False):
            user_repr = user.get_username()
        else:
            user_repr = "Anonymous"

        log_entry = f"{datetime.now()} - User: {user_repr} - Path: {request.path}\n"
        with LOG_FILE_PATH.open("a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

        response = self.get_response(request)
        return response


