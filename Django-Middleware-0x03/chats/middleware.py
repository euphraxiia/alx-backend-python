from datetime import datetime, time
from pathlib import Path

from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils import timezone


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


class RestrictAccessByTimeMiddleware:
    """
    Blocks requests outside 06:00-21:00 server-local time by returning HTTP 403.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time(6, 0)   # 6:00 AM
        self.end_time = time(21, 0)    # 9:00 PM

    def __call__(self, request):
        current_time = timezone.localtime().time()
        if not (self.start_time <= current_time < self.end_time):
            return HttpResponseForbidden(
                "Access to the messaging app is restricted between 9 PM and 6 AM."
            )
        return self.get_response(request)

