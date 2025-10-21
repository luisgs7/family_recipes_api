from rest_framework import serializers

from recipe.models import Category, Recipe


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "url", "name"]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "url",
            "title",
            "description",
            "ingredients",
            "instructions",
            "category",
            "created_at",
            "updated_at",
            "user",
        ]
