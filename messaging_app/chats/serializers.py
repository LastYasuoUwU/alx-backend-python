from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    # Add CharField example
    username = serializers.CharField(max_length=150, required=True)
    
    # Add SerializerMethodField example
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = '__all__'
    
    def get_full_name(self, obj):
        """Method for SerializerMethodField"""
        return f"{obj.first_name} {obj.last_name}" if hasattr(obj, 'first_name') else obj.username
    
    def validate_username(self, value):
        """Add validation that can raise ValidationError"""
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = '__all__'
    
    def get_sender_name(self, obj):
        """Get the sender's username"""
        return obj.sender.username if hasattr(obj, 'sender') else None
    
    def validate(self, data):
        """Validate message data"""
        if 'content' in data and not data['content'].strip():
            raise serializers.ValidationError("Message content cannot be empty")
        return data

class ConversationSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = '__all__'
    
    def get_participant_count(self, obj):
        """Get the number of participants"""
        return obj.participants.count() if hasattr(obj, 'participants') else 0
    
    def validate(self, data):
        """Validate conversation data"""
        if 'title' in data and len(data['title']) > 200:
            raise serializers.ValidationError("Title is too long")
        return data