"""Root URL configuration for the signals_project."""

from django.contrib import admin
from django.urls import path

from messaging.views import delete_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("delete-account/", delete_user, name="delete_user"),
]


