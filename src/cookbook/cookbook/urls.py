from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

import recipes.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipe/<str:slug>/', recipes.views.detail),
    path('', recipes.views.index),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
