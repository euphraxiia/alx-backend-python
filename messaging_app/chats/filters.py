import django_filters
from django_filters.rest_framework import FilterSet
from .models import Message, Conversation


class MessageFilter(FilterSet):
    """
    Filter class for messages.
    
    Filters:
    - conversation_id: Filter messages by conversation ID
    - sender_id: Filter messages by sender user ID
    - conversation_participant: Filter messages from conversations with specific user ID
    - sent_after: Filter messages sent after a specific date/time
    - sent_before: Filter messages sent before a specific date/time
    - sent_at: Filter messages sent on a specific date/time
    """
    
    # Filter by conversation ID
    conversation_id = django_filters.UUIDFilter(
        field_name='conversation__conversation_id',
        lookup_expr='exact'
    )
    
    # Filter by sender user ID
    sender_id = django_filters.UUIDFilter(
        field_name='sender__user_id',
        lookup_expr='exact'
    )
    
    # Filter messages from conversations with specific user as participant
    conversation_participant = django_filters.UUIDFilter(
        field_name='conversation__participants__user_id',
        lookup_expr='exact'
    )
    
    # Filter messages sent after a specific date/time
    sent_after = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte'
    )
    
    # Filter messages sent before a specific date/time
    sent_before = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte'
    )
    
    # Filter messages sent on a specific date (date only, not time)
    sent_at = django_filters.DateFilter(
        field_name='sent_at',
        lookup_expr='date'
    )
    
    class Meta:
        model = Message
        fields = [
            'conversation_id',
            'sender_id',
            'conversation_participant',
            'sent_after',
            'sent_before',
            'sent_at'
        ]

