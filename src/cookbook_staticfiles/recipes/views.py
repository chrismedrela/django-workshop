from django.shortcuts import get_object_or_404, render

from .models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', {'object_list': recipes})


def detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'recipes/detail.html', {'object': recipe})
