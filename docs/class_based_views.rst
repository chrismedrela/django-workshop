*****************
Class Based Views
*****************

Many views render only one query set with a template. The "manual work" in the
views for creating Querysets is therefore really superfluous. Generic views are
supposed to take over this work, making the creation of views easier. Generic
views are particularly suitable for recurring display forms, such as list views.

Class based views were introduced in Django 1.3. These are even more flexible
than the previously existing generic views, which were still based on functions.

Let's replace the two functions index and detail with class-based views in the
file ``recipes/views.py``. First two additional imports must be added:

::

    from django.views.generic import DetailView, ListView

Now the two functions ``index`` and ``detail`` are replaced by these classes:

::

    class RecipeListView(ListView):
        template_name = 'recipes/index.html'

        def get_queryset(self):
            recipes = Recipe.objects.all()
            return recipes


    class RecipeDetailView(DetailView):
        model = Recipe
        template_name = 'recipes/detail.html'

Modifying URLConf
=================

In order to use these also the URLConf ``recipes/urls.py`` must be adapted. The
two old URLs are removed and replaced by new ones at the end of the file:

::

    from django.urls import include, path

    import recipes.views

    urlpatterns = [
        path('recipe/<str:slug>/', recipes.views.RecipeDetailView.as_view(), name='recipes_recipe_detail'),
        path('create/', recipes.views.create, name='recipes_recipe_create'),
        path('edit/<int:recipe_id>/', recipes.views.edit, name='recipes_recipe_edit'),
        path('', recipes.views.RecipeListView.as_view(), name='recipes_recipe_index'),
    ]

Converting ``create`` view
==========================

``create`` view can be replaced by the following class-based view:

::

    from django.contrib.auth.mixins import LoginRequiredMixin
    from django.views.generic import CreateView

    class RecipeCreateView(LoginRequiredMixin, CreateView):
        model = Recipe
        template_name = 'recipes/form.html'
        form_class = RecipeForm

        def form_valid(self, form):
            recipe = form.save(commit=False)
            recipe.author = self.request.user
            recipe.slug = slugify(recipe.title)
            recipe.save()
            form.save_m2m()
            return super().form_valid(form)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['create'] = True
            return context

We need to modify URLConf:

::

    path('create/', recipes.views.RecipeCreateView.as_view(), name='recipes_recipe_create'),

Converting ``edit`` view
========================

``edit`` view can be replaced by the following class-based view:

::

    from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
    from django.views.generic import UpdateView

    class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
        model = Recipe
        form_class = RecipeForm
        template_name = 'recipes/form.html'
        pk_url_kwarg = 'recipe_id'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['create'] = False
            return context

        def form_valid(self, form):
            retval = super().form_valid(form)
            messages.success(self.request, 'The recipe was updated.')
            return retval
            
        def test_func(self):
            recipe = self.get_object()
            return recipe.author == self.request.user or self.request.user.is_staff

And, again, we need to modify URLConf:

::

    path('edit/<int:recipe_id>/', recipes.views.RecipeUpdateView.as_view(), name='recipes_recipe_edit'),


Further links to the Django documentation
=========================================

* :djangodocs:`Introduction to class-based views <topics/class-based-views>`
* :djangodocs:`Built-in class-based views API <ref/class-based-views>`
* `Detailed descriptions, with full methods and attributes, for each of Django's class-based generic views. <https://ccbv.co.uk/>`_
