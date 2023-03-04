from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from account.models import User
from django.core import serializers
from django.contrib.auth import authenticate
from BaseManager.baseRenderers import BaseJsonRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [BaseJsonRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        
        return Response({ 
            "message": "Registration successful",
            "data": serializer.data,
            "tokens": tokens
            }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    renderer_classes = [BaseJsonRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)
        
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        password = serializer.data.get('password')
        
        user = authenticate(email = email, password = password)
        if user is None: return Response({ "errors": "Invalid credentials" }, status=status.HTTP_400_BAD_REQUEST)
    
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "Login successful",
            "tokens": tokens
            }, status=status.HTTP_200_OK)

class UserProfileView(APIView):
  renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

