from recipe.serializers import CategorySerializer, RecipeSerializer
from rest_framework import viewsets

from recipe.models import Category, Recipe
from recipe.permissions.recipe_permissions import RecipeUserPermission

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [RecipeUserPermission]
    queryset = Category.objects.select_related("user").all()
    serializer_class = CategorySerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [RecipeUserPermission]
    queryset = Recipe.objects.select_related("category", "user").all()
    serializer_class = RecipeSerializer
