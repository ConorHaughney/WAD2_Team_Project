from django.urls import path
from Recipes import views

app_name = 'Recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipes, name='recipes'),
]
