from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Provides list, retrieve, create, update, and delete operations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    def list(self, request):
        """List all conversations"""
        conversations = self.get_queryset()
        serializer = self.serializer_class(conversations, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific conversation by ID"""
        try:
            conversation = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def create(self, request):
        """Create a new conversation"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, pk=None):
        """Update an existing conversation"""
        try:
            conversation = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(conversation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, pk=None):
        """Delete a conversation"""
        try:
            conversation = self.get_queryset().get(pk=pk)
            conversation.delete()
            return Response(
                {"message": "Conversation deleted successfully"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a specific conversation"""
        try:
            conversation = self.get_queryset().get(pk=pk)
            messages = Message.objects.filter(conversation=conversation)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Provides list, retrieve, create, update, and delete operations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def list(self, request):
        """List all messages"""
        messages = self.get_queryset()
        # Optional: filter by conversation if conversation_id is provided
        conversation_id = request.query_params.get('conversation_id', None)
        if conversation_id:
            messages = messages.filter(conversation_id=conversation_id)
        
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific message by ID"""
        try:
            message = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(message)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def create(self, request):
        """Send a new message to an existing conversation"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Verify that the conversation exists
            conversation_id = request.data.get('conversation')
            try:
                conversation = Conversation.objects.get(pk=conversation_id)
                serializer.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                )
            except Conversation.DoesNotExist:
                return Response(
                    {"error": "Conversation not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, pk=None):
        """Update an existing message"""
        try:
            message = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(message, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, pk=None):
        """Delete a message"""
        try:
            message = self.get_queryset().get(pk=pk)
            message.delete()
            return Response(
                {"message": "Message deleted successfully"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def send_to_conversation(self, request):
        """
        Custom action to send a message to a specific conversation.
        Expected payload: {
            "conversation_id": 1,
            "sender": 1,
            "content": "Hello!"
        }
        """
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender')
        content = request.data.get('content')
        
        if not all([conversation_id, sender_id, content]):
            return Response(
                {"error": "conversation_id, sender, and content are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
            sender = User.objects.get(pk=sender_id)
            
            message_data = {
                'conversation': conversation_id,
                'sender': sender_id,
                'content': content
            }
            
            serializer = self.serializer_class(data=message_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Sender not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
