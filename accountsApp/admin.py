from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Account)
admin.site.register(ForgotPassword)
admin.site.register(AvatarImages)
admin.site.register(AvatarOwnership)
