from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls'))

]

if settings.DEBUG:
    urlpattersn += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpattersn += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
