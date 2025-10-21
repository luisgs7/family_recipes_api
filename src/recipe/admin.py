from django.contrib import admin

from recipe.models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("-id",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    search_fields = ("title", "category__name")
    list_filter = ("category",)
    ordering = ("-id",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
