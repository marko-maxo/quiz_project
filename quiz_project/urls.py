"""quiz_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from Pages.views import *

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/account/', include("accountsApp.urls"), name="account"),
    path('api/quiz/', include("quizApp.urls"), name="quiz"),

    # Pages app
    path("", index, name="index"),
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),
    path("forgot_password/", forgot_password_page, name="forgot_password_page"),
    path("reset_password/<slug:reset_link>", reset_password_page, name="reset_password_page"),


    path("dashboard/", dashboard, name="dashboard"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
