from rest_framework.permissions import BasePermission

class IsAdminOrMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'member']