from rest_framework import permissions


class AdminOrReadonly(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True

    """
     def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)  # не уверен насчет user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff

     """
