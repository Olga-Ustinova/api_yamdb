from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    '''Права доступа для администратора и/или суперюзера'''
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser
            )
        )
