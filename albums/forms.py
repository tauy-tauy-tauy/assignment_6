from django import forms
from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Album title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe this album...',
            }),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'photo-file-input',
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Photo caption (optional)',
            }),
        }
