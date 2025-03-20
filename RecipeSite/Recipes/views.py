from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.urls import reverse
from Recipes.forms import RecipeForm, ReviewForm, UserForm, UserProfileForm
from Recipes.models import Recipe, Favourites, Reviews, UserProfile

# Home page showing most popular recipes
def home(request):
    popular_recipe = Recipe.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating').first()
    random_recipe = popular_recipe
    while random_recipe == popular_recipe:
        random_recipe = Recipe.objects.order_by('?').first()
    context_dict = {'popular_recipe': popular_recipe,
                    'random_recipe': random_recipe}
    
    return render(request, 'Recipes/home.html', context_dict)

# Recipe list page
def recipes(request):
    context_dict = {}
    search_query = request.GET.get('search', '')
     
    if search_query:
        recipes = Recipe.objects.filter(recipe_name__icontains=search_query)
        context_dict['recipes'] = recipes
        context_dict['search_query'] = search_query
        if not recipes:
            context_dict['all_recipes'] = Recipe.objects.all().order_by('recipe_name')
    else:
        context_dict['recipes'] = Recipe.objects.all().order_by('recipe_name')
     
    return render(request, 'Recipes/recipes.html', context=context_dict)

def create_account(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Create and save user
            user = user_form.save()
            user.set_password(user.password)  
            user.save()

            # Create and save user profile
            profile = profile_form.save(commit=False)
            profile.user = user  

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True  

            
            login(request, user)
            return redirect('Recipes:home')  

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'Recipes/create_account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })

#  Page where users can comment and rate
def show_recipe(request, recipe_name_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_name_slug)
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found", status=404)

    comments = recipe.reviews_set.all()
    avg_rating = recipe.reviews_set.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_form = ReviewForm()
    comment_form = ReviewForm()

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_form = ReviewForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.user = request.user.userprofile  
                comment.save()
                return redirect('Recipes:show_recipe', recipe_slug=recipe.slug)

        elif 'rating' in request.POST:
            rating_form = ReviewForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.recipe = recipe
                rating.user = request.user.userprofile 
                rating.save()
                return redirect('Recipes:show_recipe', recipe_slug=recipe.slug)

    context = {
        'recipe': recipe,
        'comments': comments,
        'avg_rating': avg_rating,
        'rating_form': rating_form,
        'comment_form': comment_form,
    }
    return render(request, 'Recipes/show_recipe.html', context)

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect('Recipes:home')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    
    return render(request, 'Recipes/login.html')

# Add new recipe (requires login)
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user.userprofile  
            recipe.save()
            return redirect('Recipes:show_recipe', recipe_name_slug=recipe.slug)
    else:
        form = RecipeForm()
    return render(request, 'Recipes/add_recipe.html', {'form': form})

# User logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('Recipes:home')

# Most popular recipes page
def most_popular(request):
    recipes = Recipe.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:10]
            
    context_dict = {'Recipes': recipes}
    return render(request, 'Recipes/most_popular.html', context_dict)

# User's favourite recipes
@login_required
def favourites(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    favourite_recipes = Recipe.objects.filter(favourites__user=user_profile)    
    context_dict = {'Recipes': favourite_recipes}
    return render(request, 'Recipes/your_favourites.html', context_dict)

# Add recipe to user's favourites
@login_required
def add_favourite(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found", status=404)
    
    Favourites.objects.get_or_create(user=request.user.userprofile, recipe=recipe)
    return redirect('Recipes:show_recipe', recipe_slug=recipe.slug)

# Search recipes 
def search(request):
    query = request.GET.get('query', '')
    recipes = Recipe.objects.filter(recipe_name__icontains=query) if query else []
    context_dict = {'Recipes': recipes, 'query': query}
    return render(request, 'Recipes/search_recipe.html', context_dict)

