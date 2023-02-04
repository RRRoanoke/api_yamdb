from rest_framework import permissions

from reviews.models import Role


class IsAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.role == Role.ADMIN or request.user.is_superuser
        )
