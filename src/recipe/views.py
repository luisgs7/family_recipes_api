from recipe.serializers import CategorySerializer, RecipeSerializer
from rest_framework import viewsets

from recipe.models import Category, Recipe


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related("category").all()
    serializer_class = RecipeSerializer
