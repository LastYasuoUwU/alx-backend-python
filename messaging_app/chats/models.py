from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# -------------------------
# 1️⃣ Custom User Model
# -------------------------
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds fields not defined in the built-in User model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# -------------------------
# 2️⃣ Conversation Model
# -------------------------
class Conversation(models.Model):
    """
    A conversation involving multiple participants (users).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "conversations"

    def __str__(self):
        names = ", ".join([user.email for user in self.participants.all()])
        return f"Conversation between: {names}"


# -------------------------
# 3️⃣ Message Model
# -------------------------
class Message(models.Model):
    """
    Messages exchanged in a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "messages"
        ordering = ['sent_at']

    def __str__(self):
        return f"From {self.sender.email} at {self.sent_at}: {self.message_body[:30]}"
