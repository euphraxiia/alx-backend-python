from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant, IsMessageSenderOrParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating conversations.
    
    list: List all conversations the authenticated user is a participant in
    create: Create a new conversation with participants
    retrieve: Retrieve a specific conversation
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsConversationParticipant]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at', 'conversation_id']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return conversations where the authenticated user is a participant"""
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related(
            'participants', 'messages', 'messages__sender'
        )
    
    def perform_create(self, serializer):
        """Create a conversation and ensure the current user is a participant"""
        conversation = serializer.save()
        # Ensure the current user is added as a participant if not already included
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a specific conversation"""
        conversation = self.get_object()
        messages = conversation.messages.all().select_related('sender').order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating messages.
    
    list: List all messages (optionally filtered by conversation)
    create: Send a new message to a conversation
    retrieve: Retrieve a specific message
    """
    serializer_class = MessageSerializer
    permission_classes = [IsMessageSenderOrParticipant]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__email', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at', 'message_id']
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """Return messages, optionally filtered by conversation"""
        queryset = Message.objects.select_related('sender', 'conversation')
        
        # Filter by conversation if conversation_id is provided
        conversation_id = self.request.query_params.get('conversation_id', None)
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        
        # Only return messages from conversations the user is a participant in
        user = self.request.user
        queryset = queryset.filter(conversation__participants=user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create a message and set the sender to the current user"""
        conversation = serializer.validated_data.get('conversation')
        
        # Verify the user is a participant in the conversation
        if conversation and self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        
        # Set sender to current user
        serializer.save(sender=self.request.user)
