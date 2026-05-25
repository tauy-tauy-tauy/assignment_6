from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AlbumForm, PhotoForm
from .models import Album, Photo
from .permissions import (
    can_manage_album,
    can_manage_photo,
    get_deletable_photo_ids,
    get_manageable_albums_queryset,
    get_manageable_photos_queryset,
    get_viewable_albums_queryset,
    is_album_admin,
)


class AlbumPermissionContextMixin:
    """Expose RBAC flags to templates (no permission logic in templates)."""

    def get_album_for_permissions(self):
        return getattr(self, 'album', None) or self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        album = self.get_album_for_permissions()

        context['is_album_admin'] = is_album_admin(user)
        if album is not None:
            context['can_edit_album'] = can_manage_album(user, album)
            context['can_add_photo'] = can_manage_album(user, album)
            context['can_view_album'] = True
            context['deletable_photo_ids'] = get_deletable_photo_ids(user, album)

        return context


class ViewableAlbumQuerysetMixin:
    def get_queryset(self):
        return get_viewable_albums_queryset(self.request.user)


class ManageableAlbumQuerysetMixin:
    def get_queryset(self):
        return get_manageable_albums_queryset(self.request.user)


class ManageablePhotoQuerysetMixin:
    def get_queryset(self):
        return get_manageable_photos_queryset(self.request.user)


class AlbumOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        album = self.get_object()
        return can_manage_album(self.request.user, album)


class AlbumListView(ViewableAlbumQuerysetMixin, ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_album_admin'] = is_album_admin(user)
        context['is_authenticated_user'] = user.is_authenticated
        return context


class AlbumDetailView(AlbumPermissionContextMixin, ViewableAlbumQuerysetMixin, DetailView):
    model = Album
    template_name = 'albums/album_detail.html'


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(
    LoginRequiredMixin,
    AlbumOwnerOrAdminMixin,
    ManageableAlbumQuerysetMixin,
    UpdateView,
):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'


class AlbumDeleteView(
    LoginRequiredMixin,
    AlbumOwnerOrAdminMixin,
    ManageableAlbumQuerysetMixin,
    DeleteView,
):
    model = Album
    template_name = 'albums/confirm_delete.html'
    success_url = reverse_lazy('albums:list')


class PhotoCreateView(LoginRequiredMixin, AlbumPermissionContextMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/album_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(
            get_manageable_albums_queryset(request.user),
            pk=kwargs['album_pk'],
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = self.album
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.album.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_photo_upload'] = True
        return context

    def get_album_for_permissions(self):
        return self.album


class PhotoDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    ManageablePhotoQuerysetMixin,
    DeleteView,
):
    model = Photo
    template_name = 'albums/confirm_delete.html'

    def test_func(self):
        return can_manage_photo(self.request.user, self.get_object())

    def get_success_url(self):
        return reverse('albums:detail', kwargs={'pk': self.get_object().album.pk})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
