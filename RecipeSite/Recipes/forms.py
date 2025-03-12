from django import forms
from django.contrib.auth.models import User
from Recipes.models import UserProfile, Recipe, Reviews

# User registration form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# User profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

# Add Recipe form
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cuisine', 'difficulty', 'time_taken', 'instructions', 'portion', 'picture']

# Leave a comment form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
