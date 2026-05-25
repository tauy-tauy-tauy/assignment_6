from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from cloudinary.models import CloudinaryField

User = get_user_model()


class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('albums:detail', kwargs={'pk': self.pk})


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = CloudinaryField('image', folder='photos')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return f'Photo {self.id} in {self.album.title}'

    def get_absolute_url(self):
        return reverse('albums:detail', kwargs={'pk': self.album.pk})