from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0003_alter_photo_image_cloudinary'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='is_public',
            field=models.BooleanField(
                default=False,
                help_text='Allow guests and other users to view this album (read-only).',
            ),
        ),
    ]
