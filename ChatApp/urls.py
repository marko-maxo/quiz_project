from django.urls import path
from .views import *

urlpatterns = [
    path("load_chats/", LoadChats.as_view(), name="load_chats"),
    path("load_users_chat/", LoadUsersForChat.as_view(), name="load_users_chat"),

    path("send_message_to_user/", SendMessageToUser.as_view(), name="send_message_to_user"),
    path("send_message_to_conversation/", SendMessageToConversation.as_view(), name="send_message_to_conversation"),

    path("get_conversation_messages/", LoadConversationFromConversation.as_view(), name="get_conversation_messages"),
    path("get_conversation_messages_from_user/", LoadConversationFromUser.as_view(),
         name="get_conversation_messages_from_user"),
]
