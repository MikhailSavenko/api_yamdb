from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Создание/редактирование/удаление доступно
    администратору/суперпользователю, чтение для всех.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin' or request.user.is_staff
        )


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверить, является ли пользователь аутентифицированным и является ли он администратором
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False