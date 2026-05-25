import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=cloudinary.models.CloudinaryField(
                max_length=255,
                verbose_name='image',
                folder='photos',
            ),
        ),
    ]
