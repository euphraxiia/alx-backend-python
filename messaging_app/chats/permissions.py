from rest_framework import permissions
from .models import Conversation, Message


class IsConversationParticipant(permissions.BasePermission):
    """
    Permission to ensure users can only access conversations they are participants in.
    """
    
    def has_permission(self, request, view):
        """
        Allow access if user is authenticated.
        The queryset filtering in views handles list-level filtering.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        """
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        return False


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Permission to ensure users can only access messages from conversations they are in,
    or messages they sent.
    """
    
    def has_permission(self, request, view):
        """
        Allow access if user is authenticated.
        The queryset filtering in views handles list-level filtering.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the sender or a participant in the message's conversation.
        """
        if isinstance(obj, Message):
            # User can access if they sent the message
            if obj.sender.user_id == request.user.user_id:
                return True
            
            # User can access if they are a participant in the conversation
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        
        return False


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Combined permission for both conversations and messages.
    Allows access if user is owner/sender or participant.
    """
    
    def has_permission(self, request, view):
        """
        Allow access if user is authenticated.
        The queryset filtering in views handles list-level filtering.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check permissions based on object type.
        """
        # For Conversation objects
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        
        # For Message objects
        if isinstance(obj, Message):
            # User can access if they sent the message
            if obj.sender.user_id == request.user.user_id:
                return True
            
            # User can access if they are a participant in the conversation
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        
        return False

