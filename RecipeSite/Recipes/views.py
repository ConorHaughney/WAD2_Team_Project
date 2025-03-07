from django.shortcuts import render
from django.http import HttpResponse

def test(request):
    context_dict = {}
    return render(request, 'Recipes/base.html', context=context_dict)
