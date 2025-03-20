import os
import django
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecipeSite.settings')
django.setup()

from Recipes.models import Cuisine, Difficulty, Recipe, UserProfile, Reviews
from django.contrib.auth.models import User

def populate():
    cuisines = ['Italian', 'Chinese', 'Mexican', 'French', 'Japanese']
    for cuisine_name in cuisines:
        Cuisine.objects.get_or_create(name=cuisine_name)

    difficulties = ['Easy', 'Medium', 'Hard']
    for difficulty_level in difficulties:
        Difficulty.objects.get_or_create(difficulty=difficulty_level)

    recipes_data = [
        {'name': 'Spaghetti Carbonara', 'cuisine': 'Italian', 'difficulty': 'Medium'},
        {'name': 'Kung Pao Chicken', 'cuisine': 'Chinese', 'difficulty': 'Hard'},
        {'name': 'Tacos', 'cuisine': 'Mexican', 'difficulty': 'Easy'},
        {'name': 'Ratatouille', 'cuisine': 'French', 'difficulty': 'Medium'},
        {'name': 'Sushi', 'cuisine': 'Japanese', 'difficulty': 'Hard'}
    ]

    recipes = []
    for recipe in recipes_data:
        cuisine = Cuisine.objects.get(name=recipe['cuisine'])
        difficulty = Difficulty.objects.get(difficulty=recipe['difficulty'])
        recipe_obj, _ = Recipe.objects.get_or_create(name=recipe['name'], cuisine=cuisine, difficulty=difficulty)
        recipes.append(recipe_obj)

    fake_users = [
        {'username': 'user1', 'email': 'user1@example.com'},
        {'username': 'user2', 'email': 'user2@example.com'},
        {'username': 'user3', 'email': 'user3@example.com'},
        {'username': 'user4', 'email': 'user4@example.com'},
        {'username': 'user5', 'email': 'user5@example.com'}
    ]

    user_profiles = []
    for user_data in fake_users:
        user, created = User.objects.get_or_create(username=user_data['username'], defaults={'email': user_data['email']})
        if created:
            user.set_password('password')
            user.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profiles.append(profile)

    reviews_text = [
        "Amazing recipe! I loved it.",
        "Not bad, but could use some more spices.",
        "Easy to follow and delicious.",
        "I tried this and my family loved it!",
        "Could be better, but still good overall."
    ]

    for recipe in recipes:
        for profile in user_profiles:
            if not Reviews.objects.filter(user=profile, recipe=recipe).exists():
                Reviews.objects.create(
                    user=profile,
                    recipe=recipe,
                    rating=random.randint(3, 5),
                    comment=random.choice(reviews_text)
                )

if __name__ == '__main__':
    print("Populating database with sample data, fake users, and reviews...")
    populate()
    print("Database populated successfully!")
