from django.db import models
from django import forms
from django.contrib.auth.models import User


class Chat(models.Model):
    user = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_string = models.CharField(max_length=500)


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['chat_string']
