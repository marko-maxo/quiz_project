from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete
import time
import random
import string

# from .tasks import send_verification_email

all_characters = string.ascii_letters + string.digits


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    verified = models.BooleanField(default=False)
    verification_url = models.CharField(max_length=40, blank=True, null=True)

    profile_photo = models.ImageField(upload_to="profile_images/", default="default_profile.png")

    def __str__(self):
        return self.user.username


def create_account_for_user(sender, instance, created, *args, **kwargs):
    if created:
        verification_code = ''.join(random.choice(all_characters) for x in range(30))
        Account.objects.create(
            user=instance,
            verification_url=verification_code)
        # TODO: When emails are done add this
        # send_verification_email(verification_code=verification_code, send_to_email=instance.email)


post_save.connect(create_account_for_user, sender=User)
