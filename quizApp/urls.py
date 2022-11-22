from django.urls import path
from .views import *

urlpatterns = [
    path("standard_index/", StandardQuizView.as_view(), name="standard_index")
]