from rest_framework import permissions


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
