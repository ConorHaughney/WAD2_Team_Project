from django import forms
from django.contrib.auth.models import User
from Recipes.models import UserProfile, Recipe, Reviews, Ingredients

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
    time_taken = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'min': '0',
            'required': True
        })
    )
    
    portion = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'min': '1',
            'max': '10000',
            'required': True
        })
    )
    
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your recipe instructions here...',
            'style': 'font-family: Arial, sans-serif; font-size: 14px;'
        })
    )
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cuisine', 'difficulty', 'time_taken', 'instructions', 'portion', 'picture']

# Leave a comment form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1, 
                'max': 5,
                'placeholder': 'Rate from 1-5',
                'style': 'font-family: Arial, sans-serif; font-size: 14px'
            }),
            'comment': forms.Textarea(attrs={
                'style': 'font-family: Arial, sans-serif; font-size: 14px',
                'placeholder': 'Write your review here...'
            })
        }
        
# Add ingredient form
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['ingredient_name', 'quantity']
        widgets = {
            'ingredient_name': forms.TextInput(attrs={
                'maxlength': 15,
                'required': True,
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'max': 10000,
                'required': True,
            })
        }
