from datetime import datetime, time, timedelta
from pathlib import Path
from collections import defaultdict, deque

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


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of POST (chat message) requests
    per IP address within a rolling time window.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of recent POST requests per IP
        self.requests_per_ip = defaultdict(deque)
        self.time_window = timedelta(minutes=1)
        self.max_requests = 5

    def __call__(self, request):
        # Only enforce rate limiting on POST requests (messages)
        if request.method == "POST":
            ip = self._get_client_ip(request)
            now = timezone.now()

            timestamps = self.requests_per_ip[ip]

            # Remove timestamps that are outside the time window
            while timestamps and now - timestamps[0] > self.time_window:
                timestamps.popleft()

            # If over the limit, block the request
            if len(timestamps) >= self.max_requests:
                return HttpResponseForbidden(
                    "Message limit exceeded. You can only send 5 messages per minute."
                )

            # Record current request
            timestamps.append(now)

        return self.get_response(request)

    def _get_client_ip(self, request):
        """Best-effort retrieval of client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # Take the first IP in the list
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "unknown")
        return ip


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

