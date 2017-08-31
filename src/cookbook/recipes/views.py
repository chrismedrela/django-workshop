from django.http import Http404
from django.http import HttpResponse
from django.template import Context, loader

from .models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    t = loader.get_template('recipes/index.html')
    c = {'object_list': recipes}
    return HttpResponse(t.render(c))


def detail(request, slug):
    return HttpResponse('My second view.')


def detail(request, slug):
    try:
        recipe = Recipe.objects.get(slug=slug)
    except Recipe.DoesNotExist:
        raise Http404
    t = loader.get_template('recipes/detail.html')
    c = {'object': recipe}
    return HttpResponse(t.render(c))