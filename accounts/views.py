from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import serializers, viewsets
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # 비밀번호 확인 로직
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError({'password': '비밀번호와 비밀번호 확인이 일치하지 않습니다.'})
        
        name = validated_data.pop('name')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

        user.first_name = name  # User 모델의 first_name 필드에 이름 값 저장
        user.save()
        return user

    # 회원 정보 수정
    def update(self, instance, validated_data):
    # 비밀번호 확인 로직
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)
        
        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError({'password': '비밀번호와 비밀번호 확인이 일치하지 않습니다.'})

        if password and password_confirm:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ['name','username', 'password', 'password_confirm', 'email'] # 피그마에 맞게 순서 수정
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 사용자 권한 확인
        if instance != request.user and not request.user.is_staff:
            return Response({'error': '회원 정보를 수정할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)