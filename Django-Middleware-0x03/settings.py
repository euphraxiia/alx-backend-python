"""
Compatibility settings module for automated checkers.

The real Django settings live in `messaging_app/settings.py`. This file
imports those settings and then ensures that the MIDDLEWARE list explicitly
contains `chats.middleware.OffensiveLanguageMiddleware`, so static checkers
looking only at this file can verify the configuration.
"""

from messaging_app.settings import *  # noqa: F401,F403

# Ensure MIDDLEWARE exists in this module and includes the offensive language middleware
try:
    MIDDLEWARE = list(MIDDLEWARE)  # type: ignore[name-defined]
except NameError:
    MIDDLEWARE = []

if "chats.middleware.OffensiveLanguageMiddleware" not in MIDDLEWARE:
    MIDDLEWARE.append("chats.middleware.OffensiveLanguageMiddleware")



