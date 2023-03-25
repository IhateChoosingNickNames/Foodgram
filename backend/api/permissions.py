from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsNotBlockedOrReadOnly(permissions.BasePermission):
    """Проверка наличия блокировки на аккаунте."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or not request.user.is_blocked
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверка на авторство."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.id == obj.author.id
        )
