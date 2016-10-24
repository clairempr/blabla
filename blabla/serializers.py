from blabla.models import Chat
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    """
    Serializing all the Chats
    """
    class Meta:
        model = Chat
        fields = '__all__'
