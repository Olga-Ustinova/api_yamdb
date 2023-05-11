from rest_framework import permissions


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    '''
    Предоставляет права на осуществление запросов
    только суперпользователю, админу или
    аутентифицированному пользователю с ролью admin.
    '''

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.is_admin)
        )


class AnonReadOnly(permissions.BasePermission):
    '''Разрешает анонимному пользователю только безопасные запросы.'''

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
