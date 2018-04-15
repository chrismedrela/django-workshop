from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

import recipes.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(recipes.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
