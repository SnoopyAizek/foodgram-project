from rest_framework.permissions import SAFE_METHODS, BasePermission
from foodgram.exceptions import UnauthorizedUser


class BanPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user.is_authenticated and request.user.is_active)


class AuthenticatedNoBan(BanPermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            raise UnauthorizedUser
        return True
