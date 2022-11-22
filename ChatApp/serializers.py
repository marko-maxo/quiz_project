from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ConversationModel, ChatModel, ChatMedia


class ConversationSerializer(serializers.ModelSerializer):
    chat_with = serializers.SerializerMethodField()

    class Meta:
        model = ConversationModel
        fields = ["id", "last_message", "last_message_time", "chat_with"]

    def get_chat_with(self, obj):
        if obj.all_users_chat:
            return "Everybody"
        chat_with = ""
        for p in obj.participants.all():
            if p.username == self.context["current_username"]:
                continue
            chat_with = p.username
            break
        return chat_with


class UserForChatSerializer(serializers.ModelSerializer):
    # full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = ["id", "username", "full_name"]
        fields = ["id", "username"]
    #
    # def get_full_name(self, obj):
    #     return f"{obj.first_name} {obj.last_name}"


class ChatLoadSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = ChatModel
        fields = ["id", "message_text", "timestamp", "sender"]

    def get_sender(self, member):
        user = member.sent_by
        return {"username": user.username, "email": user.email}
