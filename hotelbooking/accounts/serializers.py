from rest_framework import serializers
from .models import User,HotelPost

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')  # Add 'name' to fields

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False)
    class Meta:
        model = HotelPost
        fields = ['title','image', 'content', 'tags', 'created_at', 'updated_at']