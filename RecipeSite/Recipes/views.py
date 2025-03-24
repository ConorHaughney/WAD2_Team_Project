from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.urls import reverse
from Recipes.forms import RecipeForm, ReviewForm, UserForm, UserProfileForm
from Recipes.models import Recipe, Favourites, Reviews, UserProfile
from django.db.models.functions import Lower

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
    recipes_list = Recipe.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        recipes_list = recipes_list.filter(recipe_name__icontains=search_query)
        
    recipes_list = Recipe.objects.annotate(avg_rating=Avg('reviews__rating'))
        
    sort_options = {
        'time_asc': 'Quick Recipes First',
        'time_desc': 'Long Recipes First',
        'portion_asc': 'Small Portions First', 
        'portion_desc': 'Large Portions First',
        'name': 'Alphabetical Order'
    }
    
    sort_by = request.GET.get('sort', '')
    if sort_by == 'time_asc':
        recipes_list = recipes_list.order_by('time_taken')
    elif sort_by == 'time_desc':
        recipes_list = recipes_list.order_by('-time_taken')
    elif sort_by == 'portion_asc':
        recipes_list = recipes_list.order_by('portion')
    elif sort_by == 'portion_desc':
        recipes_list = recipes_list.order_by('-portion')
    elif sort_by == 'name':
        recipes_list = recipes_list.order_by(Lower('recipe_name'))
    else:
        recipes_list = recipes_list.order_by(Lower('recipe_name'))
    
    selected_cuisines = request.GET.getlist('cuisine')
    if selected_cuisines:
        recipes_list = recipes_list.filter(cuisine__in=selected_cuisines)
        
    selected_difficulties = request.GET.getlist('difficulty')
    if selected_difficulties:
        recipes_list = recipes_list.filter(difficulty__in=selected_difficulties)

    cuisines = Recipe.objects.values_list('cuisine', flat=True).distinct()
    difficulties = Recipe.objects.values_list('difficulty', flat=True).distinct()
    
    context_dict = {
        'recipes': recipes_list,
        'search_query': search_query,
        'cuisines': cuisines,
        'difficulties': difficulties,
        'selected_cuisines': selected_cuisines,
        'selected_difficulties': selected_difficulties,
        'sort_options': sort_options,
        'sort_by': sort_by
    }
     
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
        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = Favourites.objects.filter(
                user=request.user.userprofile, 
                recipe=recipe
            ).exists()
            
        if request.method == 'POST' and request.user.is_authenticated:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = Reviews.objects.get_or_create(
                    user=request.user.userprofile,
                    recipe=recipe,
                    defaults={'rating': request.POST.get('rating')}
                )[0]
                
                review_form = ReviewForm(request.POST, instance=review)
                review_form.save()
                return redirect('Recipes:show_recipe', recipe_name_slug=recipe_name_slug)
        else:
            review_form = ReviewForm()
            
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found", status=404)

    comments = recipe.reviews_set.all()
    avg_rating = recipe.reviews_set.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'recipe': recipe,
        'comments': comments,
        'avg_rating': avg_rating,
        'rating_form': ReviewForm(),
        'is_favorite': is_favorite,
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
                context = {'disabled_error': "Your account has been disabled"}
                return render(request, 'Recipes/login.html', context)
        else:
            context = {'login_error': "Username or password incorrect"}
            return render(request, 'Recipes/login.html', context)
    
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
def add_favourite(request, recipe_name_slug):
    if request.method == 'POST':
        try:
            recipe = Recipe.objects.get(slug=recipe_name_slug)
            user_profile = request.user.userprofile
            action = request.POST.get('action')
                
            if action == 'remove':
                Favourites.objects.filter(user=user_profile, recipe=recipe).delete()
            else:
                if not Favourites.objects.filter(user=user_profile, recipe=recipe).exists():
                    Favourites.objects.create(user=user_profile, recipe=recipe)
                        
        except Recipe.DoesNotExist:
            return HttpResponse("Recipe not found", status=404)
    return redirect('Recipes:show_recipe', recipe_name_slug=recipe_name_slug)


# Search recipes 
def search(request):
    query = request.GET.get('query', '')
    recipes = Recipe.objects.filter(recipe_name__icontains=query) if query else []
    context_dict = {'Recipes': recipes, 'query': query}
    return render(request, 'Recipes/search_recipe.html', context_dict)

