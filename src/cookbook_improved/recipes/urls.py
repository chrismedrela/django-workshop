from django.urls import path, include

import recipes.views

urlpatterns = [
    path('recipe/<str:slug>/', recipes.views.detail, name='recipes_recipe_detail'),
    path('', recipes.views.index, name='recipes_recipe_index'),
]
