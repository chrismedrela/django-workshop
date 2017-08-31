from django.conf.urls import include, url

import recipes.views

urlpatterns = [
    url(r'^recipe/(?P<slug>[-\w]+)/$', recipes.views.detail, name='recipes_recipe_detail'),
    url(r'^add/$', recipes.views.add, name='recipes_recipe_add'),
    url(r'^edit/(?P<recipe_id>\d+)/$', recipes.views.edit, name='recipes_recipe_edit'),
    url(r'^$', recipes.views.index, name='recipes_recipe_index'),
]
