from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.views import CreateView as AuthCreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Album, Photo

User = get_user_model()


class AlbumListView(ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_detail.html'


class OwnerOrGroupRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = getattr(self, 'object', None)
        if obj is None and hasattr(self, 'get_object'):
            obj = self.get_object()
        if obj is None:
            return self.request.user.is_authenticated
        return (obj.owner == self.request.user) or self.request.user.groups.filter(name='album_admin').exists()


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'description']
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, OwnerOrGroupRequiredMixin, UpdateView):
    model = Album
    fields = ['title', 'description']
    template_name = 'albums/album_form.html'


class AlbumDeleteView(LoginRequiredMixin, OwnerOrGroupRequiredMixin, DeleteView):
    model = Album
    template_name = 'albums/confirm_delete.html'
    success_url = reverse_lazy('albums:list')


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['image', 'caption']
    template_name = 'albums/album_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.album = Album.objects.get(pk=kwargs['album_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = self.album
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.album.pk})


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'albums/confirm_delete.html'

    def test_func(self):
        photo = self.get_object()
        return (photo.uploaded_by == self.request.user) or self.request.user.groups.filter(name='album_admin').exists()

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.get_object().album.pk})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        return super().form_valid(form)