from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

import recipes.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recipe/(?P<slug>[-\w]+)/$', recipes.views.detail),
    url(r'^$', recipes.views.index),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
