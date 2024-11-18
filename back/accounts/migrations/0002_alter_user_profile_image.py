# Generated by Django 4.2.16 on 2024-11-18 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.CharField(choices=[('profile_images/character_single1.jpg', 'Image 1'), ('profile_images/character_single2.jpg', 'Image 2'), ('profile_images/character_single3.jpg', 'Image 3'), ('profile_images/character_single4.jpg', 'Image 4'), ('profile_images/character_single5.jpg', 'Image 5'), ('profile_images/character_single6.jpg', 'Image 6')], default='profile_images/image1.jpg', max_length=255),
        ),
    ]
