from rest_framework.permissions import BasePermission

class IsAdminOrMember(BasePermission):
    def has_permission(self, request, view):
        # Support both admin and superuser-backed "admin" role.
        return request.user.role in ["admin", "superadmin", "member"]

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.role in ["admin", "superadmin"]:
            return True

        # Member can only modify their own product
        return obj.created_by == request.user