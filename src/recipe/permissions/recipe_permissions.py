from rest_framework.permissions import BasePermission


class RecipeUserPermission(BasePermission):
    """Allow the user to create, update and delete suas recipes, and read others recipes"""
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # For read methods (GET, HEAD, OPTIONS), allow access without authentication
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # For other methods (POST, PUT, PATCH, DELETE), require authentication and ownership
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated and request.user == obj.user
        
        return False