from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import serializers, viewsets

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(write_only=True)

    def create(self, validated_data):
        name = validated_data.pop('name')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
            
        )
        user.first_name = name  # User 모델의 first_name 필드에 이름 값 저장
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password','name']
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer