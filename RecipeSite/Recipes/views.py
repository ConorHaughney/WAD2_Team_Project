from django.shortcuts import render
from django.http import HttpResponse

from Recipes.models import Recipe



def test(request):
    context_dict = {}
    return render(request, 'Recipes/home.html', context=context_dict)



def home(request):
    context_dict = {}
    return render(request, 'Recipes/home.html', context=context_dict)



def login(request):
    context_dict = {}
    return render(request, 'Recipes/login.html', context=context_dict)



def recipes(request):
    context_dict = {}
    return render(request, 'Recipes/recipes.html', context=context_dict)



def search(request):
    context_dict = {}
    return render(request, 'Recipes/search_recipe.html', context=context_dict)



def show_recipe(request, recipe_name_slug):
    context_dict = {}

    try:
        recipe = Recipe.objects.get(slug=recipe_name_slug)

        context_dict['recipe'] = recipe
    except Recipe.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None    
    return render(request, 'Recipes/show_recipe.html', context=context_dict)



def add_recipe(request):
    context_dict = {}
    return render(request, 'Recipes/add_recipe.html', context=context_dict)



def create_account(request):
    context_dict = {}
    return render(request, 'Recipes/create_account.html', context=context_dict)

def favourites(request):
    context_dict = {}
    return render(request, 'Recipes/your_favourites.html', context=context_dict)

def most_popular(request):
    context_dict = {}
    return render(request, 'Recipes/most_popular.html', context=context_dict)