from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
from utilities.tokenFunctions import createJWT, decodeJWT
import random
import string
# from .tasks import send_verification_email

from .models import Account

all_characters = string.ascii_letters + string.digits


# Create your views here.

class RegisterView(APIView):
    http_method_names = ["post", ]
    authentication_classes = []

    def post(self, request):
        current_jwt = ""
        try:
            current_jwt = request.COOKIES["jwt"]
            if current_jwt:
                return Response({"error": "Already logged in"}, status=status.HTTP_403_FORBIDDEN)
        except:
            pass
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]
        errors = {}
        register_fail = False
        try:
            User.objects.get(email=email)
            register_fail = True
            errors["email"] = "Email is taken"
        except:
            pass

        username = email.split("@")[0] + str(random.randint(1000, 9999))

        while True:
            try:
                User.objects.get(username=username)
                username = email.split("@")[0] + str(random.randint(1000, 9999))
                continue
            except:
                break

        if len(password) < 6:
            register_fail = True
            errors["password"] = "Password has to be longer than 5 characters"

        if register_fail:
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

        new_user = User.objects.create_user(username=username, email=email, password=password)
        response = Response()
        response.set_cookie("jwt", createJWT(new_user), expires=86400)
        response.data = {"success": "Account has been created. To verify your account follow the steps in the email."}
        response.status_code = status.HTTP_200_OK
        return response


class LogoutView(APIView):
    http_method_names = ["post", ]
    authentication_classes = []

    def post(self, request):
        response = Response()
        response.set_cookie("jwt", "", expires=1)
        response.data = {"success": "Logout successful"}
        response.status_code = status.HTTP_202_ACCEPTED
        return response


class LoginView(APIView):
    http_method_names = ["post", ]
    authentication_classes = []

    def post(self, request):
        current_jwt = ""
        try:
            current_jwt = request.COOKIES["jwt"]
            if current_jwt:
                return Response({"error": "Already logged in"}, status=status.HTTP_403_FORBIDDEN)
        except:
            pass
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]

        try:
            the_user = User.objects.get(email=email)
        except:
            return Response({"error": "Wrong credentials, please try again"}, status=status.HTTP_400_BAD_REQUEST)

        if not the_user.check_password(password):
            return Response({"error": "Wrong credentials, please try again"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response()
        response.set_cookie("jwt", createJWT(the_user), expires=86400)
        response.data = {"success": "Login successful"}
        response.status_code = status.HTTP_200_OK
        return response


class VerifyView(APIView):
    http_method_names = ["get", ]
    authentication_classes = []

    def get(self, request, verify_code):
        try:
            account_for_verification = Account.objects.get(verification_url=verify_code)
        except:
            return Response({"error": "Verification code is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        account_for_verification.verified = True
        account_for_verification.save()
        return Response({"success": "Account has been verified"}, status=status.HTTP_202_ACCEPTED)


class LoginCheck(APIView):
    http_method_names = ["get", ]

    def get(self, request):
        account = Account.objects.get(user=request.user)
        return Response({"success": "You are logged in",
                         "user": {"username": request.user.username, "email": request.user.email,
                                  "verified": account.verified}})


class ChangePasswordView(APIView):
    http_method_names = ["post", ]

    def post(self, request):
        data = json.loads(request.body)
        try:
            old_password = data["old_password"]
            new_password = data["new_password"]
            if len(new_password) < 6:
                return Response({"error": "Password has to be at least 6 characters long"},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Input old and new password"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if not user.check_password(old_password):
            return Response({"error": "Current password is not correct"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"success": "Password has been updated"}, status=status.HTTP_202_ACCEPTED)


class ChangeEmailView(APIView):
    http_method_names = ["post", ]

    def post(self, request):
        data = json.loads(request.body)
        try:
            new_email = data["new_email"]
        except:
            return Response({"error": "New email is not provided"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            User.objects.get(email=new_email)
            return Response({"error": "Email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        user.email = new_email
        account = Account.objects.get(user=user)
        account.can_rate = False
        account.verified = False
        account.verification_url = ''.join(random.choice(all_characters) for x in range(30))
        user.save()
        account.save()
        # TODO: When emails are done add this
        # send_verification_email(verification_code=account.verification_url, send_to_email=request.user.email)
        return Response({"success": "Email has been updated. To verify your account follow the steps in the email."},
                        status=status.HTTP_202_ACCEPTED)
