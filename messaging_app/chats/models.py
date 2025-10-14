from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# -------------------------
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True,editable=False)
    first_name = models.CharField(max_length=30,null=False)
    last_name = models.CharField(max_length=30,null=False)
    email = models.EmailField(unique=True,null=False)
    password = models.CharField(max_length=128,null=False)
    phone_number= models.CharField(max_length=15,null=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']


class Message(models.Model):
    message_id = models.AutoField(primary_key=True,editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sent_messages')
    message_body = models.TextField(null=False)
    sent_at = models.TimeField(default=timezone.now)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    participants_id =models.ManyToManyField(User,related_name='conversations')
    create_at = models.TimeField(default=timezone.now)
