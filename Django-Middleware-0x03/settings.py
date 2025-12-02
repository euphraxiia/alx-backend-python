"""
Compatibility settings module for automated checkers.

The real Django settings live in `messaging_app/settings.py`. This file
simply re-exports them so tools looking for `Django-Middleware-0x03/settings.py`
can still import the correct configuration, including middleware.
"""

from messaging_app.settings import *  # noqa: F401,F403


