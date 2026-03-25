from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'member'