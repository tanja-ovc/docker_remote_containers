from rest_framework import permissions


class AdminPermissions(permissions.BasePermission):
    """
    Права на создание, удаление и изменение пользователей.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_administrator)


class AdminOrReadOnly(permissions.BasePermission):
    """
    Права для админов на создание произведений, категорий и жанров.
    Права для всех на чтение.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_administrator
                or request.method in permissions.SAFE_METHODS)


class AdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    """
    Права на чтение есть у всех.
    Права на запись есть только у:
        1) авторов ревью и комментов;
        2) модераторов;
        3) админов.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_administrator
                or request.user.is_superuser)


class SelfOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_administrator
