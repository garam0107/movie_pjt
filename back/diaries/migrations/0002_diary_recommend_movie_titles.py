# Generated by Django 4.2.16 on 2024-11-22 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='recommend_movie_titles',
            field=models.TextField(blank=True),
        ),
    ]