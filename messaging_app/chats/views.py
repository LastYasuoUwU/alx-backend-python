from .models import User, Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer

from rest_framework import generics

class ConversationViewSet(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer