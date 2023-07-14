from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Создание/редактирование/удаление доступно
    администратору/суперпользователю, чтение для всех.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin)


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверить, является ли пользователь аутентифицированным и является ли он администратором
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False
    

class CommentReviewsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешение чтения комментариев анонимным пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение чтения, создания, редактирования и удаления комментариев
        # для аутентифицированных пользователей
        elif request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        # Разрешение редактирования или удаления своего комментария
        if request.method in ['PUT', 'PATCH', 'DELETE'] and obj.author == request.user:
            return True
        # Разрешение модератору редактировать или удалять комментарии
        elif request.method in ['PUT', 'PATCH', 'DELETE'] and request.user.role == 'moderator':
            return True
        # Разрешение администратору редактировать или удалять комментарии
        elif request.method in ['PUT', 'PATCH', 'DELETE'] and request.user.role == 'admin':
            return True
        return False
    

