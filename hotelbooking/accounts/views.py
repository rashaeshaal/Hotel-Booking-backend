from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model  
from .serializers import UserSerializer
from .serializers import UserSerializer,PostSerializer
from .models import User,HotelPost
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
   

        user = User.objects.filter(email=email).first()  # This line will now work

        if user is None:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Incorrect password!'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'is_superuser': user.is_superuser
            },
            'token': str(refresh.access_token)  
        })
        

class PostCreateView(APIView):
    def post(self, request):
        print("Request data:", request.data)  

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=None)  
            print("Post created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateHotelPostView(APIView):
    permission_classes = [IsAuthenticated]  

    def patch(self, request, pk):  
        post = get_object_or_404(HotelPost, pk=pk)
    
        if post.author != request.user:
            return Response({"detail": "You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    
class HotelPostListView(ListAPIView):
    queryset = HotelPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  
    
    
class HotelPostDetailView(generics.RetrieveAPIView):
    queryset = HotelPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny] 
    lookup_field = 'id' 
    
class UpdateHotelPostView(APIView):
    permission_classes = [IsAuthenticated]  

    def patch(self, request, pk): 
        post = get_object_or_404(HotelPost, pk=pk)
        
        
        if post.author != request.user:
            return Response({"detail": "You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        
       
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         
import logging

logger = logging.getLogger(__name__)                  
class DeleteHotelPostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = get_object_or_404(HotelPost, pk=pk)
        
        if post.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        

        logger.info(f"User {request.user} deleted post {post.title}")
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)