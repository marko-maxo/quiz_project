import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
import random
import string

from .models import ConversationModel, ChatModel, ChatMedia
from utilities.permClasses import IsVerified
from .serializers import ConversationSerializer, UserForChatSerializer, ChatLoadSerializer

channel_layer = get_channel_layer()


# Create your views here.

class LoadChats(APIView):
    http_method_names = ["get", ]
    permission_classes = [IsVerified, ]

    def get(self, request):
        user = request.user

        main_group_chat = ConversationModel.objects.filter(all_users_chat=True)
        user_existing_chats = ConversationModel.objects.filter(participants=user).order_by("-last_message_time")

        main_group_chat_serialized = ConversationSerializer(main_group_chat,
                                                            context={'current_username': request.user.username},
                                                            many=True).data
        user_existing_chats_serialized = ConversationSerializer(user_existing_chats,
                                                                context={'current_username': request.user.username},
                                                                many=True).data

        return Response({"chats": main_group_chat_serialized + user_existing_chats_serialized})


class LoadUsersForChat(ListAPIView):
    http_method_names = ["get", ]
    permission_classes = [IsVerified, ]
    serializer_class = UserForChatSerializer

    def get_queryset(self):
        username_search = self.request.query_params.get("search")
        if username_search is None:
            username_search = ""
        return User.objects.filter(username__istartswith=username_search).exclude(id=self.request.user.id)


class SendMessageToUser(APIView):
    http_method_names = ["post", ]
    permission_classes = [IsVerified, ]

    def post(self, request):
        user_sending = request.user
        data = json.loads(request.body)

        sending_to_user = int(data["sending_to_user"])
        message_text = data["message_text"]

        try:
            conversation = ConversationModel.objects.get(
                Q(one_one_chat_string=f"{sending_to_user}-{user_sending.id}") | Q(
                    one_one_chat_string=f"{user_sending.id}-{sending_to_user}"))
        except:
            conversation = ConversationModel.objects.create(one_one_chat_string=f"{user_sending.id}-{sending_to_user}")
            conversation.participants.add(user_sending)
            conversation.participants.add(User.objects.get(id=sending_to_user))

        chat_message = ChatModel.objects.create(conversation=conversation, sent_by=user_sending,
                                                message_text=message_text)

        message_to_send = {
            "type": "chat",
            "message_text": message_text,
            "timestamp": str(chat_message.timestamp),
            "sent_by_username": chat_message.sent_by.username,
            "conversation_id": conversation.id,
            "message_id": chat_message.id,
        }

        if conversation.all_users_chat:
            print("SENDING TO EVERYONE")
            async_to_sync(channel_layer.group_send)(
                "chat-all",
                {
                    "type": "sending_a_message",
                    "message": message_to_send,
                }
            )

            return Response({"success": "Message has been sent to everyone", "message_text": message_text})

        for participant in conversation.participants.all():
            print("Participant:", participant.id)
            async_to_sync(channel_layer.group_send)(
                f"chat-{participant.id}",
                {
                    "type": "sending_a_message",
                    "message": message_to_send,
                }
            )

        return Response({"success": "Message has been sent", "message_text": message_text})


class SendMessageToConversation(APIView):
    http_method_names = ["post", ]
    permission_classes = [IsVerified, ]

    def post(self, request):
        user_sending = request.user
        data = json.loads(request.body)

        sending_to_conversation = int(data["sending_to_conversation"])
        message_text = data["message_text"]

        try:
            conversation = ConversationModel.objects.get(id=sending_to_conversation)
            if conversation.all_users_chat:
                pass
            else:
                if str(user_sending.id) not in conversation.one_one_chat_string.split("-"):
                    return Response({"error": "User is not part of the conversation"}, status=status.HTTP_403_FORBIDDEN)

        except:
            return Response({"error": "Conversation doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        chat_message = ChatModel.objects.create(conversation=conversation, sent_by=user_sending,
                                                message_text=message_text)

        message_to_send = {
            "type": "chat",
            "message_text": message_text,
            "timestamp": str(chat_message.timestamp),
            "sent_by_username": chat_message.sent_by.username,
            "conversation_id": conversation.id,
            "message_id": chat_message.id,
        }

        if conversation.all_users_chat:
            print("SENDING TO EVERYONE")
            async_to_sync(channel_layer.group_send)(
                "chat-all",
                {
                    "type": "sending_a_message",
                    "message": message_to_send,
                }
            )

            return Response({"success": "Message has been sent to everyone", "message_text": message_text})

        for participant in conversation.participants.all():
            print("Participant:", participant.id)
            async_to_sync(channel_layer.group_send)(
                f"chat-{participant.id}",
                {
                    "type": "sending_a_message",
                    "message": message_to_send,
                }
            )

        return Response({"success": "Message has been sent", "message_text": message_text})


class LoadConversationFromConversation(APIView):
    http_method_names = ["get", ]
    permission_classes = [IsVerified, ]

    def get(self, request):
        user = request.user

        conversation_id = int(request.query_params['conversation'])
        page = int(request.query_params['page'])

        try:
            conversation = ConversationModel.objects.get(id=conversation_id)
            if conversation.all_users_chat:
                pass
            else:
                conversation = ConversationModel.objects.get(id=conversation_id, participants=user)

            chat = ChatModel.objects.filter(conversation=conversation).order_by("-id")[(page - 1) * 10:page * 10]
            serialized = ChatLoadSerializer(chat, many=True)

            if conversation.all_users_chat:
                chat_participants = "ALL"
            else:
                chat_participants = [user.username for user in conversation.participants.all()]

            results = {"conversation": conversation.id, "chat_participants": chat_participants,
                       "messages": serialized.data}
            return Response({"results": results})
        except Exception as e:
            return Response({"error": "User is not part of the conversation", "e": str(e)})


class LoadConversationFromUser(APIView):
    http_method_names = ["get", ]
    permission_classes = [IsVerified, ]

    def get(self, request):
        user = request.user

        other_user = int(request.query_params['other_user'])
        page = int(request.query_params['page'])

        try:
            conversation = ConversationModel.objects.get(
                Q(one_one_chat_string=f"{user.id}-{other_user}") | Q(one_one_chat_string=f"{other_user}-{user.id}"))

            chat = ChatModel.objects.filter(conversation=conversation).order_by("-id")[(page - 1) * 10:page * 10]
            serialized = ChatLoadSerializer(chat, many=True)

            chat_participants = [user.username for user in conversation.participants.all()]

            results = {"conversation": conversation.id, "chat_participants": chat_participants,
                       "messages": serialized.data}
            return Response({"results": results})
        except Exception as e:
            return Response({"error": "Conversation doesn't exist", "e": str(e)})
