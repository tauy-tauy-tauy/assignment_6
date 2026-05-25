from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from albums.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('', include('albums.urls')),
    path('', RedirectView.as_view(pattern_name='albums:list', permanent=False)),
]

if settings.DEBUG and not all(settings.CLOUDINARY.values()):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)