from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.role == request.user.UserRole.ADMIN
            )
        return False


class OnlyAdminCanChangeRole(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.role == obj.UserRole.ADMIN:
            return True
        if 'role' not in request.data:
            return True
        return False
