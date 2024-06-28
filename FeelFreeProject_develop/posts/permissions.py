#게시글/댓글 수정 및 삭제 사용자 권한 부여 
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 누구나 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 쓰기 권한은 작성자
        return obj.writer == request.user
