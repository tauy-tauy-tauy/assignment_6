from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps


class Command(BaseCommand):
    help = 'Create album_admin group and assign model permissions'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='album_admin')
        Album = apps.get_model('albums', 'Album')
        Photo = apps.get_model('albums', 'Photo')
        perms = Permission.objects.filter(content_type__app_label='albums', content_type__model__in=['album', 'photo'])
        group.permissions.set(perms)
        group.save()
        self.stdout.write(self.style.SUCCESS('album_admin group created/updated'))