import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecipeSite.settings')
django.setup()

from Recipes.models import Cuisine, Difficulty, Recipe

def populate():
    cuisines = ['Italian', 'Chinese', 'Mexican', 'French', 'Japanese']
    for cuisine_name in cuisines:
        Cuisine.objects.get_or_create(name=cuisine_name)

    difficulties = ['Easy', 'Medium', 'Hard']
    for difficulty_level in difficulties:
        Difficulty.objects.get_or_create(difficulty=difficulty_level)

    recipes = [
        {'name': 'Spaghetti Carbonara', 'cuisine': 'Italian', 'difficulty': 'Medium'},
        {'name': 'Kung Pao Chicken', 'cuisine': 'Chinese', 'difficulty': 'Hard'},
        {'name': 'Tacos', 'cuisine': 'Mexican', 'difficulty': 'Easy'},
        {'name': 'Ratatouille', 'cuisine': 'French', 'difficulty': 'Medium'},
        {'name': 'Sushi', 'cuisine': 'Japanese', 'difficulty': 'Hard'}
    ]

    for recipe in recipes:
        cuisine = Cuisine.objects.get(name=recipe['cuisine'])
        difficulty = Difficulty.objects.get(difficulty=recipe['difficulty'])
        Recipe.objects.get_or_create(name=recipe['name'], cuisine=cuisine, difficulty=difficulty)

if __name__ == '__main__':
    print("Populating database...")
    populate()
    print("Database populated successfully!")