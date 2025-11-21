import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model extending AbstractUser
    
    Inherits from AbstractUser:
    - password: stores password hash (VARCHAR, NOT NULL)
    - Other standard Django user fields
    
    Additional fields defined:
    - user_id, first_name, last_name, email, phone_number, role, created_at
    """
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    username = None  # Remove username field since we use email
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False, db_index=True)
    # password field is inherited from AbstractUser (stores password hash)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        null=False,
        default='guest'
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    # Override username to use email instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email'),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """Conversation model tracking which users are involved"""
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'conversation'
        indexes = [
            models.Index(fields=['conversation_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        participant_names = ', '.join([
            f"{p.first_name} {p.last_name}" 
            for p in self.participants.all()[:3]
        ])
        return f"Conversation {self.conversation_id} - {participant_names}"


class Message(models.Model):
    """Message model containing sender and conversation"""
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        db_index=True
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        db_index=True
    )
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'message'
        indexes = [
            models.Index(fields=['message_id']),
            models.Index(fields=['sender']),
            models.Index(fields=['conversation']),
            models.Index(fields=['sent_at']),
        ]
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Message from {self.sender.first_name} at {self.sent_at}"
