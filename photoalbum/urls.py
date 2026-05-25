from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from albums.views import RegisterView
from photoalbum.auth_views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path(
        'accounts/logout/',
        LogoutView.as_view(next_page=reverse_lazy('albums:list')),
        name='logout',
    ),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('', include('albums.urls')),
    path('', RedirectView.as_view(pattern_name='albums:list', permanent=False)),
]