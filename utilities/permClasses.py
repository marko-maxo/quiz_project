from rest_framework import permissions

from accountsApp.models import Account


class IsVerified(permissions.BasePermission):
    message = "You are not verified"

    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        return account.verified
