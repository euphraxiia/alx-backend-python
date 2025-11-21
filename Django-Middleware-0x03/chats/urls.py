from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import ConversationViewSet, MessageViewSet

# Create a DefaultRouter instance to automatically generate URL patterns for viewsets
router = routers.DefaultRouter()

# Register viewsets with the router
# This automatically creates URL patterns for list, create, retrieve, update, partial_update, and destroy actions
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a nested router for messages under conversations
# NestedDefaultRouter allows messages to be nested under conversations
messages_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Also register messages at the top level for direct access
router.register(r'messages', MessageViewSet, basename='message')

# Include the router URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(messages_router.urls)),
]

