from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import recipes.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'cookbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^recipe/(?P<slug>[-\w]+)/$', recipes.views.detail),
    url(r'^$', recipes.views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
