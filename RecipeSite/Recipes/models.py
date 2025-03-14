from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator



class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username



class Cuisine(models.Model):
    NAME_MAX_LENGTH = 25

    name = models.CharField(max_length=NAME_MAX_LENGTH, primary_key=True)

    class Meta:
        verbose_name_plural = 'Cuisines'

    def __str__(self):
        return self.name
    


class Difficulty(models.Model):
    DIFFICULTY_MAX_LENGTH = 15

    difficulty = models.CharField(max_length=DIFFICULTY_MAX_LENGTH, primary_key=True)

    def __str__(self):
        return self.difficulty
    
    class Meta:
        verbose_name_plural = 'Difficulties'

    


class Recipe(models.Model):
    RECIPE_NAME_MAX_LENGTH = 40
    
    recipe_name = models.CharField(max_length=RECIPE_NAME_MAX_LENGTH, unique=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    time_taken = models.IntegerField()
    instructions = models.TextField()
    portion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    picture = models.ImageField(upload_to='recipe_images', blank=False)
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.recipe_name)
        super(Recipe, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.recipe_name 



class Ingredients(models.Model):
    INGREDIENT_NAME_MAX_LENGTH = 15

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=INGREDIENT_NAME_MAX_LENGTH)
    quantity = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return self.ingredient_name
    
    class Meta:
        verbose_name_plural = 'Ingredients'
    
    

class Favourites(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe.recipe_name
    
    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name_plural = 'Favourites'
    


class Reviews(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.comment
    
    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name_plural = 'Reviews'
