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