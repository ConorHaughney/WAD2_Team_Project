from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from Recipes.models import Recipe

from Recipes.forms import UserForm, UserProfileForm



def test(request):
    context_dict = {}
    return render(request, 'Recipes/home.html', context=context_dict)



def home(request):
    context_dict = {}
    return render(request, 'Recipes/home.html', context=context_dict)



def recipes(request):
    context_dict = {}
    search_query = request.GET.get('search', '')
    
    if search_query:
        recipes = Recipe.objects.filter(recipe_name__icontains=search_query)
        context_dict['recipes'] = recipes
        context_dict['search_query'] = search_query
    else:
        context_dict['recipes'] = Recipe.objects.all()
    
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
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
        
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'Recipes/create_account.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

def favourites(request):
    context_dict = {}
    return render(request, 'Recipes/your_favourites.html', context=context_dict)

def most_popular(request):
    context_dict = {}
    return render(request, 'Recipes/most_popular.html', context=context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('Recipes:home'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
        
    else:
        return render(request, 'Recipes/login.html')
    
@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse('Recipes:home'))