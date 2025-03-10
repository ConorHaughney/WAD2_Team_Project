from django.urls import path
from Recipes import views

app_name = 'Recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('recipes/', views.recipes, name='recipes'),
    path('search/', views.search, name='search'),
    path('register/', views.create_account, name='create_account'),
    path('recipes/most_popular/', views.most_popular, name='most_popular'),
    path('recipes/your-favourites/', views.favourites, name='favourites'),
    path('recipes/add-your-own/', views.add_recipe, name='add_recipe'),
    path('recipes/<slug:recipe_name_slug>/',
         views.show_recipe, name='show_recipe'),
    
]
