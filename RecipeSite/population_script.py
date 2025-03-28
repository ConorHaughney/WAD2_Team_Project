import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecipeSite.settings')
django.setup()

from Recipes.models import Cuisine, Difficulty, Recipe, Ingredients, UserProfile, Reviews
from django.contrib.auth.models import User

def populate():
    # populate the cuisines table
    cuisines = ['Italian', 'Chinese', 'Mexican', 'French', 'Japanese', 'Vegetarian']
    for cuisine_name in cuisines:
        Cuisine.objects.get_or_create(name=cuisine_name)
    
    # populates the difficulty table
    difficulties = ['Easy', 'Medium', 'Hard']
    for level in difficulties:
        Difficulty.objects.get_or_create(difficulty=level)
    
    # creates a generic user used to upload recipes
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('password')
        user.save()
    author, created = UserProfile.objects.get_or_create(user=user)

    # creates a generic user used to review recipes
    reviewer, created = User.objects.get_or_create(
        username='reviewer',
        defaults={'email': 'reviewer@example.com'}
    )
    if created:
        reviewer.set_password('password')
        reviewer.save()
    reviewer_profile, created = UserProfile.objects.get_or_create(user=reviewer)
    
    # creates 6 recipes information
    recipes = [
        {
            'recipe_name': 'Spaghetti Carbonara',
            'cuisine': 'Italian',
            'difficulty': 'Medium',
            'time_taken': 30,
            'instructions': ("Bring a large pot of salted water to a boil and cook spaghetti until al dente. "
                "Meanwhile, in a bowl, whisk together eggs, grated Parmesan, a pinch of salt, and plenty of black pepper. "
                "In a separate pan, fry diced pancetta until crispy. "
                "Once the pasta is cooked, reserve a cup of pasta water and drain the pasta. "
                "Add the hot pasta to the pan with pancetta and remove the pan from heat. "
                "Quickly stir in the egg mixture, tossing vigorously so the residual heat gently cooks the eggs into a creamy sauce. "
                "Adjust the sauce consistency with reserved pasta water if needed. "
                "Serve immediately with an extra sprinkle of Parmesan and freshly ground pepper."),
            'portion': 4,
            'picture': 'recipe_images/spaghetti_carbonara.jpg'
        },
        {
            'recipe_name': 'Kung Pao Chicken',
            'cuisine': 'Chinese',
            'difficulty': 'Hard',
            'time_taken': 45,
            'instructions': ("Cut chicken into bite-size pieces and marinate briefly with soy sauce and cornstarch. "
                "Heat oil in a wok over high heat and stir-fry the chicken until it starts to brown. "
                "Add diced bell peppers, dried chili peppers, and chopped garlic and ginger. "
                "Stir in a sauce made from soy sauce, vinegar, sugar, and a splash of water. "
                "Toss in roasted peanuts at the end and stir-fry for another minute. "
                "Adjust seasoning if needed and serve hot over steamed rice."),
            'portion': 4,
            'picture': 'recipe_images/kung_pao_chicken.jpg'
        },
        {
            'recipe_name': 'Tacos',
            'cuisine': 'Mexican',
            'difficulty': 'Easy',
            'time_taken': 20,
            'instructions': ("Season ground beef with cumin, chili powder, and garlic. "
                "Sauté the beef until fully browned and set aside. "
                "Warm tortillas on a skillet. "
                "Prepare toppings such as diced tomatoes, shredded lettuce, cheese, and salsa. "
                "Assemble tacos by layering the beef and your preferred toppings on each tortilla. "
                "Finish with a squeeze of lime and enjoy immediately."),
            'portion': 4,
            'picture': 'recipe_images/tacos.jpg'
        },
        {
            'recipe_name': 'Ratatouille',
            'cuisine': 'French',
            'difficulty': 'Medium',
            'time_taken': 60,
            'instructions': ("Preheat your oven to 375°F (190°C). "
                "Slice zucchini, eggplant, bell peppers, and tomatoes into uniform rounds. "
                "Spread a thin layer of tomato sauce on a baking dish and arrange the vegetable slices in a concentric pattern, alternating colors. "
                "Drizzle olive oil over the vegetables and season with salt, pepper, and herbs de Provence. "
                "Cover with foil and bake for 30 minutes, then remove the foil and bake for an additional 15 minutes until the vegetables are tender. "
                "Garnish with fresh basil before serving."),
            'portion': 4,
            'picture': 'recipe_images/ratatouille.jpg'
        },
        {
            'recipe_name': 'Sushi',
            'cuisine': 'Japanese',
            'difficulty': 'Hard',
            'time_taken': 90,
            'instructions': ("Rinse sushi rice under cold water until the water runs clear, then cook according to package instructions. "
                "Mix rice vinegar, sugar, and salt in a small saucepan and heat until dissolved; gently fold this seasoning into the warm rice. "
                "Lay a sheet of nori on a bamboo mat, spread an even layer of seasoned rice over the nori, leaving a small margin at the top. "
                "Place slices of fresh fish and vegetables (such as cucumber or avocado) along the bottom edge. "
                "Roll tightly using the bamboo mat, then slice into bite-sized pieces. "
                "Serve with soy sauce, wasabi, and pickled ginger."),
            'portion': 4,
            'picture': 'recipe_images/sushi.jpg'
        },
        {
            'recipe_name': 'Mac and Cheese ',
            'cuisine': 'Vegetarian',
            'difficulty': 'Medium',
            'time_taken': 45,
            'instructions': ("Cook the macaroni in a large saucepan of boiling salted. Drain well and set aside. "
                "Melt the butter over a medium heat in a saucepan slightly larger than that used for the macaroni. Add the flour and stir to form a roux, cooking for a few minutes. "
                "Gradually whisk in the milk, a little at a time. Cook to a thickened and smooth sauce. "
                "Meanwhile, preheat the grill to hot. "
                "Remove the sauce from the hob, add 175g of the cheddar and stir until it is well combined and melted."
                "Add the macaroni to the sauce and mix well. Transfer to a deep suitably-sized ovenproof dish."
                "Sprinkle over the remaining cheddar and the Parmesan and place the dish under the hot grill. Cook until the cheese is browned and bubbling. Serve straightaway."),
            'portion': 4,
            'picture': 'recipe_images/macandcheese.jpg'
        }
    ]
    
    # creates the ingredients for the recipes
    recipe_ingredients = {
        'Spaghetti Carbonara': [
            {'ingredient_name': 'Spaghetti', 'quantity': Decimal('200')},
            {'ingredient_name': 'Eggs', 'quantity': Decimal('200')},
            {'ingredient_name': 'Pancetta', 'quantity': Decimal('100')},
            {'ingredient_name': 'Parmesan', 'quantity': Decimal('50')}
        ],
        'Kung Pao Chicken': [
            {'ingredient_name': 'Chicken', 'quantity': Decimal('300')},
            {'ingredient_name': 'Peanuts', 'quantity': Decimal('50')},
            {'ingredient_name': 'Chili Peppers', 'quantity': Decimal('10')},
            {'ingredient_name': 'Sauce', 'quantity': Decimal('30')}
        ],
        'Tacos': [
            {'ingredient_name': 'Tortillas', 'quantity': Decimal('4')},
            {'ingredient_name': 'Beef', 'quantity': Decimal('200')},
            {'ingredient_name': 'Lettuce', 'quantity': Decimal('50')},
            {'ingredient_name': 'Cheese', 'quantity': Decimal('30')}
        ],
        'Ratatouille': [
            {'ingredient_name': 'Zucchini', 'quantity': Decimal('100')},
            {'ingredient_name': 'Eggplant', 'quantity': Decimal('100')},
            {'ingredient_name': 'Bell Pepper', 'quantity': Decimal('50')},
            {'ingredient_name': 'Tomato', 'quantity': Decimal('100')}
        ],
        'Sushi': [
            {'ingredient_name': 'Rice', 'quantity': Decimal('200')},
            {'ingredient_name': 'Fish', 'quantity': Decimal('150')},
            {'ingredient_name': 'Seaweed', 'quantity': Decimal('10')},
            {'ingredient_name': 'Soy Sauce', 'quantity': Decimal('20')}
        ],
        'Mac and Cheese ': [
            {'ingredient_name': 'Macaroni', 'quantity': Decimal('250')},
            {'ingredient_name': 'Butter', 'quantity': Decimal('40')},
            {'ingredient_name': 'Plain Flour', 'quantity': Decimal('40')},
            {'ingredient_name': 'Cheddar', 'quantity': Decimal('250')},
            {'ingredient_name': 'Parmesan', 'quantity': Decimal('250')}
        ]
    }

    # creates the info for the reviews of the recipes
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
        ],
        'Mac and Cheese ': [
            {'rating': 5, 'comment': 'The mac and cheese was really good'}
        ]
    }
    
    # populates the recipes into the recipe table
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
        
        # populates the ingredients for each recipe
        if r['recipe_name'] in recipe_ingredients:
            for ing in recipe_ingredients[r['recipe_name']]:
                Ingredients.objects.get_or_create(
                    recipe=recipe_instance,
                    ingredient_name=ing['ingredient_name'],
                    quantity=ing['quantity']
                )

        # populates the reviews for each recipe
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
