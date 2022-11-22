from django.urls import path
from .views import *

urlpatterns = [
    # Account login
    path("create_user/", RegisterView.as_view(), name="create_user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login_user/", LoginView.as_view(), name="login"),
    path("verify/<str:verify_code>", VerifyView.as_view(), name="verify"),
    path("login_check/", LoginCheck.as_view(), name="login_check"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("change_email/", ChangeEmailView.as_view(), name="change_email"),

    # Icon logic
    path("show_all_icons/", ShowAllIconsView.as_view(), name="show_all_icons"),
    path("buy_icon/", BuyIconView.as_view(), name="buy_icon"),
    path("set_icon/", SetIconView.as_view(), name="set_icon"),
]
