from django.shortcuts import render
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer 
from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly # type: ignore  #작성자만 

# 게시글 
class PostViewSet(ModelViewSet): 
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] #게시물 권한 설정

    def perform_create(self, serializer): 
        serializer.save(writer = self.request.user)

# 댓글
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] #댓글 권한 설정

    def perform_create(self, serializer):  
        serializer.save(writer = self.request.user)

    def get_queryset(self, **kwargs): 
        id = self.kwargs['post_id']
        return self.queryset.filter(post=id)