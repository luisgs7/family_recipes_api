from rest_framework.permissions import BasePermission


class SuperUserPermission(BasePermission):
    """Allow the user to update suas own profile"""

    def has_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request):
        if request.user.is_superuser:
            return True
        return False
