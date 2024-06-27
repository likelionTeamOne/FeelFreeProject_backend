from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer