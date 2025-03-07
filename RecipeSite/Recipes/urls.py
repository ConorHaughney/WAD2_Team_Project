from django.urls import path
from Recipes import views

app_name = 'Recipes'

urlpatterns = [
    path('', views.test, name='test'),
]
