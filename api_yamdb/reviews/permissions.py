from rest_framework import permissions


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # if obj.owner == request.user or request.user.role in ('moderator' or 'admin'):
            # return True
        if (
            obj.owner == request.user
            or request.user.is_admin
            or request.user.is_moderator
        ):
            return True
