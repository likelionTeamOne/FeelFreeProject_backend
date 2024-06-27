from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    # 객체 소유자만이 해당 객체를 볼 수 있고 편집할 수 있도록 허용/ 삭제는 항상 불가
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH']:
            return obj.pk == request.user.pk
        elif request.method == 'DELETE':
            return False
        else:
            return True
