from django.contrib import admin
from .models import UserProfile, Cuisine, Difficulty, Recipe, Ingredients

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture')

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('difficulty',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_name', 'cuisine', 'difficulty') 
    search_fields = ('recipe_name',)
    list_filter = ('cuisine', 'difficulty')
    list_per_page = 20
    ordering = ('recipe_name',)

@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient_name', 'quantity')
    ordering = ('recipe',)