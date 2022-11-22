from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class StandardQuizView(APIView):
    def get(self, request):
        return Response({"success": "OK"})
