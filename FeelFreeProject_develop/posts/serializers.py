from rest_framework import serializers
from rest_framework.serializers import ModelSerializer 
from .models import Post, Comment 
from django.contrib.auth.models import User

class PostSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source = 'writer.username')
    
    class Meta:
        model = Post 
        fields = [ 'id', 'title', 'content' ,'writer'] 

class CommentSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source = 'writer.username')

    class Meta:
        model = Comment
        fields = [ 'id', 'comment', 'post', 'writer']