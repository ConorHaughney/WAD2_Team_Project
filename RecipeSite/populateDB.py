import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecipeSite.settings')
django.setup()

from Recipes.models import Cuisine, Difficulty, Recipe, Ingredients, UserProfile, Reviews
from django.contrib.auth.models import User

def populate():
    cuisines = ['Italian', 'Chinese', 'Mexican', 'French', 'Japanese']
    for cuisine_name in cuisines:
        Cuisine.objects.get_or_create(name=cuisine_name)
    
    difficulties = ['Easy', 'Medium', 'Hard']
    for level in difficulties:
        Difficulty.objects.get_or_create(difficulty=level)
    
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('password')
        user.save()
    author, created = UserProfile.objects.get_or_create(user=user)

    reviewer, created = User.objects.get_or_create(
        username='reviewer',
        defaults={'email': 'reviewer@example.com'}
    )
    if created:
        reviewer.set_password('password')
        reviewer.save()
    reviewer_profile, created = UserProfile.objects.get_or_create(user=reviewer)
    
    recipes = [
        {
            'recipe_name': 'Spaghetti Carbonara',
            'cuisine': 'Italian',
            'difficulty': 'Medium',
            'time_taken': 30,
            'instructions': 'Boil pasta. Mix eggs and cheese. Combine with pancetta.',
            'portion': 4,
            'picture': 'recipe_images/spaghetti_carbonara.jpg'
        },
        {
            'recipe_name': 'Kung Pao Chicken',
            'cuisine': 'Chinese',
            'difficulty': 'Hard',
            'time_taken': 45,
            'instructions': 'Stir-fry chicken. Add peanuts, chili peppers, sauce, and vegetables.',
            'portion': 4,
            'picture': 'recipe_images/kung_pao_chicken.jpg'
        },
        {
            'recipe_name': 'Tacos',
            'cuisine': 'Mexican',
            'difficulty': 'Easy',
            'time_taken': 20,
            'instructions': 'Prepare meat, salsa, and tortillas. Assemble tacos.',
            'portion': 4,
            'picture': 'recipe_images/tacos.jpg'
        },
        {
            'recipe_name': 'Ratatouille',
            'cuisine': 'French',
            'difficulty': 'Medium',
            'time_taken': 60,
            'instructions': 'Layer sliced vegetables. Bake with herbs.',
            'portion': 4,
            'picture': 'recipe_images/ratatouille.jpg'
        },
        {
            'recipe_name': 'Sushi',
            'cuisine': 'Japanese',
            'difficulty': 'Hard',
            'time_taken': 90,
            'instructions': 'Prepare rice, slice fish, and roll sushi.',
            'portion': 4,
            'picture': 'recipe_images/sushi.jpg'
        }
    ]
    
    recipe_ingredients = {
        'Spaghetti Carbonara': [
            {'ingredient_name': 'Spaghetti', 'quantity': Decimal('200.0')},
            {'ingredient_name': 'Eggs', 'quantity': Decimal('2.0')},
            {'ingredient_name': 'Pancetta', 'quantity': Decimal('100.0')},
            {'ingredient_name': 'Parmesan', 'quantity': Decimal('50.0')}
        ],
        'Kung Pao Chicken': [
            {'ingredient_name': 'Chicken', 'quantity': Decimal('300.0')},
            {'ingredient_name': 'Peanuts', 'quantity': Decimal('50.0')},
            {'ingredient_name': 'Chili Peppers', 'quantity': Decimal('10.0')},
            {'ingredient_name': 'Sauce', 'quantity': Decimal('30.0')}
        ],
        'Tacos': [
            {'ingredient_name': 'Tortillas', 'quantity': Decimal('4.0')},
            {'ingredient_name': 'Beef', 'quantity': Decimal('200.0')},
            {'ingredient_name': 'Lettuce', 'quantity': Decimal('50.0')},
            {'ingredient_name': 'Cheese', 'quantity': Decimal('30.0')}
        ],
        'Ratatouille': [
            {'ingredient_name': 'Zucchini', 'quantity': Decimal('100.0')},
            {'ingredient_name': 'Eggplant', 'quantity': Decimal('100.0')},
            {'ingredient_name': 'Bell Pepper', 'quantity': Decimal('50.0')},
            {'ingredient_name': 'Tomato', 'quantity': Decimal('100.0')}
        ],
        'Sushi': [
            {'ingredient_name': 'Rice', 'quantity': Decimal('200.0')},
            {'ingredient_name': 'Fish', 'quantity': Decimal('150.0')},
            {'ingredient_name': 'Seaweed', 'quantity': Decimal('10.0')},
            {'ingredient_name': 'Soy Sauce', 'quantity': Decimal('20.0')}
        ]
    }

    reviews = {
        'Spaghetti Carbonara': [
            {'rating': 4, 'comment': 'Delicious and creamy.'}
        ],
        'Kung Pao Chicken': [
            {'rating': 3, 'comment': 'Good, but too spicy for my taste.'}
        ],
        'Tacos': [
            {'rating': 5, 'comment': 'Amazing tacos, loved every bite!'}
        ],
        'Ratatouille': [
            {'rating': 4, 'comment': 'Fresh, tasty, and well balanced.'}
        ],
        'Sushi': [
            {'rating': 5, 'comment': 'Best sushi I have ever had!'}
        ]
    }
    
    for r in recipes:
        cuisine = Cuisine.objects.get(name=r['cuisine'])
        difficulty = Difficulty.objects.get(difficulty=r['difficulty'])
        recipe_instance, created = Recipe.objects.get_or_create(
            recipe_name=r['recipe_name'],
            cuisine=cuisine,
            author=author,
            difficulty=difficulty,
            time_taken=r['time_taken'],
            instructions=r['instructions'],
            portion=r['portion'],
            picture=r['picture']
        )
        
        if r['recipe_name'] in recipe_ingredients:
            for ing in recipe_ingredients[r['recipe_name']]:
                Ingredients.objects.get_or_create(
                    recipe=recipe_instance,
                    ingredient_name=ing['ingredient_name'],
                    quantity=ing['quantity']
                )

        if r['recipe_name'] in reviews:
            for rev in reviews[r['recipe_name']]:
                Reviews.objects.get_or_create(
                    user=reviewer_profile,
                    recipe=recipe_instance,
                    rating=rev['rating'],
                    comment=rev['comment']
                )

if __name__ == '__main__':
    print("Populating database...")
    populate()
    print("Database populated successfully!")
