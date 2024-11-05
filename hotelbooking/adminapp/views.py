from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


# Create your views here.

class AdminLoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser:
            return Response({'error': 'Access denied. Only superusers can log in.'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'email': user.email,  # Add more user data as needed
                'name': user.get_full_name(),  # Use the get_full_name method to get the full name
                'is_superuser': user.is_superuser,
            },
            'token': str(refresh.access_token)  # Token generation
        }, status=status.HTTP_200_OK)
        
