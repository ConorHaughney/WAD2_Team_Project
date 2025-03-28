from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


# table for the users profile
class UserProfile(models.Model):
    # contains the user and their profile picture
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


# table for food cuisines
class Cuisine(models.Model):
    NAME_MAX_LENGTH = 25

    # holds the name of the cuisine
    name = models.CharField(max_length=NAME_MAX_LENGTH, primary_key=True)

    class Meta:
        verbose_name_plural = 'Cuisines'

    def __str__(self):
        return self.name
    

# table for the difficulties of the recipes
class Difficulty(models.Model):
    DIFFICULTY_MAX_LENGTH = 15

    # contains the name of the difficulty (such as easy, medium, hard)
    difficulty = models.CharField(max_length=DIFFICULTY_MAX_LENGTH, primary_key=True)

    def __str__(self):
        return self.difficulty
    
    class Meta:
        verbose_name_plural = 'Difficulties'

    

# table for the actual recipes
class Recipe(models.Model):
    RECIPE_NAME_MAX_LENGTH = 40
    
    # contains the name, cuisine type, who made it, difficulty, length of time, 
    # the instructions, number of serving, the image, and a unique slug used for its url
    recipe_name = models.CharField(max_length=RECIPE_NAME_MAX_LENGTH, unique=True, error_messages={'unique': 'This recipe name is already taken. Please choose a different name.'})
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    time_taken = models.IntegerField()
    instructions = models.TextField()
    portion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    picture = models.ImageField(upload_to='recipe_images', blank=False)
    slug = models.SlugField(unique=True)

    # ability to save a recipe
    def save(self, *args, **kwargs):
        self.slug = slugify(self.recipe_name)
        super(Recipe, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.recipe_name 


# table for each recipes ingredients
class Ingredients(models.Model):
    INGREDIENT_NAME_MAX_LENGTH = 15

    # contains which recipe it belongs to, name of ingredient and its quantity
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=INGREDIENT_NAME_MAX_LENGTH)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])

    def __str__(self):
        return self.ingredient_name
    
    class Meta:
        verbose_name_plural = 'Ingredients'
    
    
# table for users favourites recipes
class Favourites(models.Model):
    # contains the user that favourited it and which recipe they favourited
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe.recipe_name
    
    class Meta:
        # each user can only favourite the recipe once, prevents duplicates
        unique_together = ('user', 'recipe')
        verbose_name_plural = 'Favourites'
    

# table for the reviews of each recipe
class Reviews(models.Model):
    # contains who reviews it, which recipe they reviewed, their comment and the rating they gave
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.comment
    
    class Meta:
        # each user can only comment on a specific recipe once, prevents duplicates
        unique_together = ('user', 'recipe')
        verbose_name_plural = 'Reviews'
