**********
Pagination
**********

Django provides a few classes that help you manage paginated data – that is,
data that's split across several pages, with "Previous/Next" links. We'll
paginate recipes list.

Pagination on ListView
======================

ListViews has already implemented support for pagination. All you have to do is
to add one class attribute:

::

    class RecipeListView(ListView):
        template_name = 'recipes/index.html'
        paginate_by = 5

        def get_queryset(self):
            recipes = Recipe.objects.all()
            logger.debug('Recipes count: %d' % recipes.count())
            return recipes

And modify ``recipes/index.html`` template:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - List of recipes{% endblock %}

    {% block content %}
    <h2>List of recipes</h2>
    <ul>
        {% for recipe in object_list %}
        <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>
        {% endfor %}
    </ul>
    {% if is_paginated %}
        <div class="pagination">
            <span class="page-links">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}">previous</a>
                {% endif %}
                <span class="page-current">
                    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
                </span>
                {% if page_obj.has_next %}
                    <a href="?page={{ page_obj.next_page_number }}">next</a>
                {% endif %}
            </span>
        </div>
    {% endif %}
    {% endblock %}

Pagination in function-based views 
==================================

Here is an example implementation of pagination for function-based recipes list
view (``index``). You can see this is much more complicated than using
class-based views. 

::

    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from django.shortcuts import render

    def index(request):
        recipes_list = Recipe.objects.all()

        paginator = Paginator(recipes_list, 5) # Show 5 recipes per page
        page = request.GET.get('page')
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            recipes = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            recipes = paginator.page(paginator.num_pages)

        return render(request, 'recipes/index.html', {'object_list': recipes, 'page_obj': recipes})

In this case you need to replace:

::

    {% if is_paginated %}

with:

::

    {% if page_obj.paginator.num_pages != 1 %}

Further links to the Django documentation
=========================================

- :djangodocs:`Documentation on Pagination <topics/pagination/>`