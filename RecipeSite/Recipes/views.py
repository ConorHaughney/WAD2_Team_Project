from django.shortcuts import render
from django.http import HttpResponse

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