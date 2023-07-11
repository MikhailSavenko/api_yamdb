from rest_framework.permissions import BasePermission


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        # Проверить, является ли пользователь аутентифицированным и является ли он администратором
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False