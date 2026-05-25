from django.db.models import Q

from .models import Album, Photo

ALBUM_ADMIN_GROUP = 'album_admin'


def is_album_admin(user):
    return (
        user.is_authenticated
        and user.groups.filter(name=ALBUM_ADMIN_GROUP).exists()
    )


def get_viewable_albums_queryset(user):
    """Albums a user may view (list/detail): own, public, or all if admin."""
    if is_album_admin(user):
        return Album.objects.all()
    if user.is_authenticated:
        return Album.objects.filter(Q(owner=user) | Q(is_public=True))
    return Album.objects.filter(is_public=True)


def get_manageable_albums_queryset(user):
    """Albums a user may create photos in or edit/delete."""
    if not user.is_authenticated:
        return Album.objects.none()
    if is_album_admin(user):
        return Album.objects.all()
    return Album.objects.filter(owner=user)


def get_manageable_photos_queryset(user):
    """Photos a user may delete."""
    if not user.is_authenticated:
        return Photo.objects.none()
    if is_album_admin(user):
        return Photo.objects.all()
    return Photo.objects.filter(
        Q(uploaded_by=user) | Q(album__owner=user)
    )


def can_view_album(user, album):
    if is_album_admin(user):
        return True
    if album.is_public:
        return True
    return user.is_authenticated and album.owner_id == user.pk


def can_manage_album(user, album):
    if not user.is_authenticated:
        return False
    if is_album_admin(user):
        return True
    return album.owner_id == user.pk


def can_manage_photo(user, photo):
    if not user.is_authenticated:
        return False
    if is_album_admin(user):
        return True
    if photo.album.owner_id == user.pk:
        return True
    return photo.uploaded_by_id == user.pk


def get_deletable_photo_ids(user, album):
    return set(
        get_manageable_photos_queryset(user)
        .filter(album=album)
        .values_list('pk', flat=True)
    )
