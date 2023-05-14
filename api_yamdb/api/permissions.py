from rest_framework import permissions


class AuthorModerAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class AnonReadOrIsAdminOnly(permissions.BasePermission):
    '''
    Разрешины безопасные запросы для Анонимных пользователей.
    Не безопасные запросы разрешены только Админу и СуперЮзеру
    '''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser
                )
            )
        )


class IsAdmin(permissions.BasePermission):
    '''Права доступа для администратора и/или суперюзера'''
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser
            )
        )
