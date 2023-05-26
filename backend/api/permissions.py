from foodgram.exceptions import UnauthorizedUser
from rest_framework.permissions import SAFE_METHODS, BasePermission


class BanPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user.is_authenticated and request.user.is_active)


class AuthenticatedNoBan(BanPermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise UnauthorizedUser
        return True


class AuthorNoBanOrAdmin(BanPermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.user.is_staff)
