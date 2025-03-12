from django import forms
from django.contrib.auth.models import User
from Recipes.models import UserProfile, Recipe, Reviews

# User registration form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        help_texts = {'username': '',}
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
            
        return cleaned_data

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
