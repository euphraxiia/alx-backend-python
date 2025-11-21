from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.SerializerMethodField()
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at', 'full_name']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def get_full_name(self, obj):
        """Return the full name of the user"""
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_email(self, value):
        """Validate email field"""
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested sender information"""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=False)
    message_body = serializers.CharField(required=True, allow_blank=False)
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_id',
            'conversation',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']
        extra_kwargs = {
            'conversation': {'required': True},
        }
    
    def validate_message_body(self, value):
        """Validate message body is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Message body must contain at least one character.")
        return value.strip()
    
    def validate(self, data):
        """Validate that sender_id exists if provided"""
        sender_id = data.get('sender_id')
        if sender_id:
            try:
                User.objects.get(user_id=sender_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"sender_id": "User with this ID does not exist."})
        return data


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested participants and messages"""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_ids',
            'participant_count',
            'messages',
            'message_count',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at', 'message_count', 'participant_count']
    
    def get_message_count(self, obj):
        """Return the count of messages in the conversation"""
        return obj.messages.count()
    
    def get_participant_count(self, obj):
        """Return the count of participants in the conversation"""
        return obj.participants.count()
    
    def validate_participant_ids(self, value):
        """Validate participant IDs exist and are unique"""
        if not value:
            raise serializers.ValidationError("At least one participant is required.")
        
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate participant IDs are not allowed.")
        
        # Check if all participant IDs exist
        existing_users = User.objects.filter(user_id__in=value)
        existing_ids = set(existing_users.values_list('user_id', flat=True))
        missing_ids = set(value) - existing_ids
        
        if missing_ids:
            raise serializers.ValidationError(
                f"Users with the following IDs do not exist: {', '.join(str(id) for id in missing_ids)}"
            )
        
        return value
    
    def create(self, validated_data):
        """Override create to handle many-to-many participants relationship"""
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        return conversation
    
    def update(self, instance, validated_data):
        """Override update to handle many-to-many participants relationship"""
        participant_ids = validated_data.pop('participant_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if participant_ids is not None:
            participants = User.objects.filter(user_id__in=participant_ids)
            instance.participants.set(participants)
        
        return instance

