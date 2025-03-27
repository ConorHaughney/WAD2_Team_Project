from django.test import TestCase

from django.db.models import Avg

from django.contrib.auth.models import User

from Recipes.models import UserProfile, Cuisine, Difficulty, Recipe, Ingredients, Favourites, Reviews

from Recipes.forms import UserForm, RecipeForm, ReviewForm

from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile

import os 




class RecipeTestCase(TestCase):

 

    def setUp(self):

        """Set up the test data for models, forms, and views."""
        # Create test user and user profile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user)

        # Create test cuisines and difficulties
        self.cuisine_italian = Cuisine.objects.create(name='Italian')
        self.cuisine_chinese = Cuisine.objects.create(name='Chinese')
        self.difficulty_easy = Difficulty.objects.create(difficulty='Easy')
        self.difficulty_medium = Difficulty.objects.create(difficulty='Medium')

 

        # Create test recipe

        self.recipe = Recipe.objects.create(

            recipe_name='Spaghetti Carbonara',

            cuisine=self.cuisine_italian,

            author=self.user_profile,

            difficulty=self.difficulty_easy,

            time_taken=30,

            instructions='Cook pasta and mix with sauce.',

            portion=2,

            picture='spaghetti.jpg',

            slug='spaghetti-carbonara'

        )

 

        # Create ingredients for the recipe

        self.ingredient_1 = Ingredients.objects.create(

            recipe=self.recipe,

            ingredient_name='Spaghetti',

            quantity=200

        )

        self.ingredient_2 = Ingredients.objects.create(

            recipe=self.recipe,

            ingredient_name='Eggs',

            quantity=3

        )

 

        # Create a favorite entry for the user

        self.favorite = Favourites.objects.create(

            user=self.user_profile,

            recipe=self.recipe

        )

 

        # Create a review for the recipe

        self.review = Reviews.objects.create(

            user=self.user_profile,

            recipe=self.recipe,

            comment='Delicious recipe!',

            rating=5

        )

 

    # --- Model Tests ---

 

    def test_recipe_creation(self):

        """Test if the recipe is created successfully."""

        recipe = Recipe.objects.get(recipe_name='Spaghetti Carbonara')

        self.assertEqual(recipe.recipe_name, 'Spaghetti Carbonara')

        self.assertEqual(recipe.cuisine.name, 'Italian')

        self.assertEqual(recipe.difficulty.difficulty, 'Easy')

        self.assertEqual(recipe.time_taken, 30)

        self.assertEqual(recipe.portion, 2)

        self.assertEqual(recipe.slug, 'spaghetti-carbonara')

 

    def test_ingredient_creation(self):

        """Test if ingredients are correctly associated with the recipe."""

        ingredient = Ingredients.objects.get(ingredient_name='Spaghetti')

        self.assertEqual(ingredient.recipe.recipe_name, 'Spaghetti Carbonara')

        self.assertEqual(ingredient.quantity, 200)

 

    def test_favorite_creation(self):

        """Test if the favorite was created correctly."""

        favorite = Favourites.objects.get(user=self.user_profile, recipe=self.recipe)

        self.assertEqual(favorite.recipe.recipe_name, 'Spaghetti Carbonara')

 

    def test_review_creation(self):

        """Test if the review was created correctly."""

        review = Reviews.objects.get(user=self.user_profile, recipe=self.recipe)

        self.assertEqual(review.comment, 'Delicious recipe!')

        self.assertEqual(review.rating, 5)

 

    def test_recipe_slug_creation(self):

        """Test if the slug was automatically generated from the recipe name."""

        recipe = Recipe.objects.get(recipe_name='Spaghetti Carbonara')

        self.assertEqual(recipe.slug, 'spaghetti-carbonara')

 

    def test_recipe_name_uniqueness(self):

        """Test that recipes with the same name can't be created."""

        duplicate_recipe = Recipe(

            recipe_name='Spaghetti Carbonara',

            cuisine=self.cuisine_italian,

            author=self.user_profile,

            difficulty=self.difficulty_medium,

            time_taken=45,

            instructions='Cook noodles and mix.',

            portion=3,

            picture='spaghetti2.jpg',

            slug='spaghetti-carbonara-2'

        )

        with self.assertRaises(Exception):

            duplicate_recipe.save()

 

    # --- Form Tests ---

 

    def test_user_form_valid(self):

        """Test if the UserForm is valid."""

        form_data = {

            'username': 'newuser',

            'email': 'test@example.com',

            'password': 'testpassword',

            'confirm_password': 'testpassword',

        }

        form = UserForm(data=form_data)

        self.assertTrue(form.is_valid())

 

    def test_user_form_invalid_password(self):

        """Test if the UserForm catches password mismatch."""

        form_data = {

            'username': 'newuser',

            'email': 'test@example.com',

            'password': 'testpassword',

            'confirm_password': 'wrongpassword',

        }

        form = UserForm(data=form_data)

        self.assertFalse(form.is_valid())

 

    def test_recipe_form_valid(self):

        """Test if the RecipeForm is valid."""

        image_path = os.path.join('media', 'recipe_images', 'spaghetti_carbonara.jpg')

 

        with open(image_path, "rb") as img_file:

            image = SimpleUploadedFile("spaghetti_carbonara.jpg", img_file.read(), content_type="image/jpeg")

 

        form_data = {

            'recipe_name': 'New Recipe',

            'cuisine': self.cuisine_italian,

            'difficulty': self.difficulty_medium,

            'time_taken': 30,

            'instructions': 'Test instructions',

            'portion': 4,

        }

        form_files = {'picture': image} 

        form = RecipeForm(data=form_data, files=form_files)

        print(form.errors)

        self.assertTrue(form.is_valid())

 

    def test_review_form_valid(self):

        """Test if the ReviewForm is valid."""

        form_data = {

            'rating': 5,

            'comment': 'Amazing!',

        }

        form = ReviewForm(data=form_data)

        self.assertTrue(form.is_valid())

 

    # --- View Tests ---

    def test_home_view(self):

        """Test home page loads successfully and contains popular and random recipes."""

        response = self.client.get(reverse('Recipes:home'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'Recipes/home.html')

        self.assertContains(response, 'Spaghetti Carbonara')

 

    def test_home_view_no_recipes(self):

        """Test home view when no recipes exist."""

        Recipe.objects.all().delete()

        response = self.client.get(reverse("Recipes:home"))

        self.assertEqual(response.status_code, 200)

       

 

    def test_popular_recipe_logic(self):

        """Test that the correct popular recipe is selected based on average rating."""

        avg_rating = Recipe.objects.get(slug='spaghetti-carbonara').reviews_set.aggregate(Avg('rating'))['rating__avg']

        self.assertEqual(avg_rating, 5.0)

        response = self.client.get(reverse('Recipes:home'))

        self.assertEqual(response.context["popular_recipe"].recipe_name, "Spaghetti Carbonara")

  

    def test_login_view(self):

        """Test that the login view works and redirects to the correct page."""

        response = self.client.post(reverse('Recipes:login'), {'username': 'testuser', 'password': 'password'})

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('Recipes:home'))

    

    def test_logout_view(self):

        """Test that the logout view works and redirects to the home page."""

        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('Recipes:logout'))

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('Recipes:home'))

   

    def test_add_recipe_view_unauthenticated(self):

        """Test that unauthenticated users cannot access recipe creation."""

        response = self.client.get(reverse('Recipes:add_recipe'))

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('Recipes:login') + '?next=' + reverse('Recipes:add_recipe')) 

    

    def test_favorite_recipe(self):

        """Test adding and removing a recipe from favorites."""

        self.client.login(username='testuser', password='password')

 

        # Add recipe to favorites

        response = self.client.post(reverse('Recipes:add_favourite', kwargs={'recipe_name_slug': self.recipe.slug}), {'action': 'add'})

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Favourites.objects.filter(user=self.user_profile, recipe=self.recipe).exists())

 

        # Remove recipe from favorites

        response = self.client.post(reverse('Recipes:add_favourite', kwargs={'recipe_name_slug': self.recipe.slug}), {'action': 'remove'})

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Favourites.objects.filter(user=self.user_profile, recipe=self.recipe).exists())

 

    def test_show_recipe_invalid_slug(self):

        """Test accessing a recipe that does not exist returns 404."""

        response = self.client.get(reverse('Recipes:show_recipe', kwargs={'recipe_name_slug': 'non-existent-recipe'}))

        self.assertEqual(response.status_code, 404)

   

    def test_create_account(self):

        """Test user registration process."""

        response = self.client.post(reverse('Recipes:create_account'), {

            'username': 'newuser',

            'password': 'TestPass123',

            'confirm_password': 'TestPass123',

            'email': 'newuser@example.com'

        }, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(User.objects.filter(username='newuser').exists())

   

    def test_show_recipe_view(self):

        """Test that the show recipe page loads correctly."""

        response = self.client.get(reverse('Recipes:show_recipe', kwargs={'recipe_name_slug': self.recipe.slug}))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'Recipes/show_recipe.html')

        self.assertContains(response, 'Spaghetti Carbonara')

   

    def test_add_review(self):

        """Test that an authenticated user can add a review."""

        self.client.login(username='testuser', password='password')

        response = self.client.post(reverse('Recipes:show_recipe', kwargs={'recipe_name_slug': self.recipe.slug}), {

            'rating': 4,

            'comment': 'Tasty recipe!'

        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Reviews.objects.filter(user=self.user_profile, recipe=self.recipe, comment='Tasty recipe!').exists())