from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet

# 게시글
post_router = SimpleRouter(trailing_slash=False)
post_router.register('posts', PostViewSet, basename='post')

# 댓글
comment_router = SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(post_router.urls)),
    path('posts/<int:post_id>/', include(comment_router.urls)),
]