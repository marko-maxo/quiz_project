from unicodedata import name

from django.urls import re_path, path
from . import consumers

urlpatterns = [
    path('wsbe/chat/', consumers.ChatConsumer.as_asgi()),
]
