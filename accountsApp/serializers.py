from rest_framework import serializers
from .models import Account, AvatarOwnership, AvatarImages


class AvatarSerializer(serializers.ModelSerializer):
    account_owns = serializers.SerializerMethodField()

    class Meta:
        model = AvatarImages
        fields = "__all__"
        extra_fields = ["account_owns"]

    def get_account_owns(self, obj):
        if AvatarOwnership.objects.filter(account=self.context['account'], avatar=obj):
            return True
        return False
