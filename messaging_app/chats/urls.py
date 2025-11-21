from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create a DefaultRouter instance to automatically generate URL patterns for viewsets
router = routers.DefaultRouter()

# Register viewsets with the router
# This automatically creates URL patterns for list, create, retrieve, update, partial_update, and destroy actions
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include the router URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]

