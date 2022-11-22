from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete
import time
import random
import string

# from .tasks import send_verification_email

all_characters = string.ascii_letters + string.digits


# Create your models here.
class AvatarImages(models.Model):
    avatar_image = models.ImageField(upload_to="profile_images/", null=False, blank=False)
    free_coins = models.BooleanField(default=True)
    cost = models.PositiveSmallIntegerField(default=0)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    verified = models.BooleanField(default=False)
    verification_url = models.CharField(max_length=40, blank=True, null=True)

    profile_photo = models.ForeignKey(AvatarImages, on_delete=models.SET_NULL, null=True, blank=True)

    silver_coins = models.PositiveIntegerField(default=100)  # Free coins
    gold_coins = models.PositiveIntegerField(default=20)  # Paid coins

    # Implement later
    xp = models.FloatField(default=0)
    level = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username


class AvatarOwnership(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    avatar = models.ForeignKey(AvatarImages, on_delete=models.CASCADE)
    owned_since = models.FloatField(default=0)


def create_account_for_user(sender, instance, created, *args, **kwargs):
    if created:
        verification_code = ''.join(random.choice(all_characters) for x in range(30))
        Account.objects.create(
            user=instance,
            verification_url=verification_code)
        # TODO: When emails are done add this
        # send_verification_email(verification_code=verification_code, send_to_email=instance.email)


def got_avatar_timestamp(sender, instance, created, *args, **kwargs):
    if created:
        instance.owned_since = time.time()
        instance.save()


post_save.connect(create_account_for_user, sender=User)
post_save.connect(got_avatar_timestamp, sender=AvatarOwnership)
