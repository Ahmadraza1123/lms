from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allow access only to Admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsLibrarian(permissions.BasePermission):
    """
    Allow access to Librarian and Admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['librarian', 'admin']


class IsMember(permissions.BasePermission):
    """
    Allow access only to Member users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'member'


class IsAuthenticatedReadOnly(permissions.BasePermission):
    """
    Allow safe (read-only) methods for any authenticated user.
    Example: GET books is allowed for all, but write restricted.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return False
