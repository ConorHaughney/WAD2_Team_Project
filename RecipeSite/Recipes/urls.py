from django.urls import path
from Recipes import views

app_name = 'Recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('recipes/', views.recipes, name='recipes'),
    path('search/', views.search, name='search'),
]
