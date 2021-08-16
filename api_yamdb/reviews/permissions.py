from rest_framework import permissions



class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated # there is permissions.IsAuthenticated for this check
        )


    # This method should be rewritten! Have a look at User.UserRole fields use them, not hardcode!
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.owner == request.user or request.user.role in ('moderator' or 'admin'):
            return True
