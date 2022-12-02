from django.shortcuts import render, redirect, reverse, HttpResponse
from utilities.tokenFunctions import decodeJWT


def checkLogin(request, redirect_to_dashboard=False):
    try:
        current_jwt = request.COOKIES["jwt"]
        if current_jwt and decodeJWT(current_jwt)[0]:
            return True
    except:
        return False


# Create your views here.
def index(request):
    # if checkLogin(request):
    #     return redirect(reverse("dashboard"))
    return render(request, "homepages/index.html")


def login_page(request):
    if checkLogin(request):
        return redirect(reverse("dashboard"))
    return render(request, "homepages/login_register/login.html")


def register_page(request):
    if checkLogin(request):
        return redirect(reverse("dashboard"))
    return render(request, "homepages/login_register/register.html")


def forgot_password_page(request):
    if checkLogin(request):
        return redirect(reverse("dashboard"))
    return render(request, "homepages/login_register/forgot_password.html")


def reset_password_page(request, reset_link):
    if checkLogin(request):
        return redirect(reverse("dashboard"))
    return render(request, "homepages/login_register/reset_password.html", {"reset_link": reset_link})


def dashboard(request):
    if not checkLogin(request):
        return redirect(reverse("login_page"))
    return render(request, "user_pages/dashboard.html")
