from custom_user.models import User
from django.db import models


class Category(models.Model):
    """Model representing a category of recipes"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=False)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Model representing a recipe"""

    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=False)

    class Meta:
        db_table = "recipes"
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id} - {self.title} ({self.category.name})"
