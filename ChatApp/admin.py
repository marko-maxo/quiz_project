from django.contrib import admin
from .models import ConversationModel, ChatModel, ChatMedia

# Register your models here.

admin.site.register(ConversationModel)
admin.site.register(ChatModel)
admin.site.register(ChatMedia)
