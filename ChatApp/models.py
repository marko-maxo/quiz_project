from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import time


# Create your models here.

class ConversationModel(models.Model):
    participants = models.ManyToManyField(User, related_name="participants", null=True, blank=True)
    all_users_chat = models.BooleanField(default=False)
    chat_name = models.CharField(max_length=120, null=True, blank=True, default=None)  # For groups
    one_one_chat_string = models.CharField(max_length=20, blank=True, null=True, default=None)  # For 1v1 search
    last_message = models.TextField(default="", blank=True, null=True)
    last_message_time = models.FloatField(null=True, default=0)


class ChatMedia(models.Model):
    file = models.FileField(upload_to="chat_media", default=None, null=True, blank=True)
    document_name = models.CharField(max_length=125, blank=True, null=True)


class ChatModel(models.Model):
    # timestamp = models.DateTimeField(auto_now_add=True)
    timestamp = models.FloatField(null=True)
    conversation = models.ForeignKey(ConversationModel, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message_text = models.TextField(null=True, blank=True)
    has_documents = models.BooleanField(default=False)
    the_documents = models.ManyToManyField(ChatMedia, blank=True)


def timestamp_the_message(sender, instance, created, *args, **kwargs):
    if created:
        now = time.time()
        instance.timestamp = now
        conv = instance.conversation
        conv.last_message = instance.message_text
        conv.last_message_time = now
        instance.save()
        conv.save()


post_save.connect(timestamp_the_message, sender=ChatModel)
