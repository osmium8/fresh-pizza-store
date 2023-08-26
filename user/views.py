from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.contrib.auth import logout, login
from drf_spectacular.utils import extend_schema

# rest_framework
from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer

# User model
User = get_user_model()

class LogoutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"Message": "Successfully Logged out"}, status=200)
    
class IsAuthenticatedAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, *args, **kwargs):
        print(request.user)
        if (request.user.is_authenticated):
            return Response({"status": True}, status=200)
        else:
            return Response({"status": False}, status=200)
    
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
