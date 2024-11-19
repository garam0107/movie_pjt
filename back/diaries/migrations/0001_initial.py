# Generated by Django 4.2.16 on 2024-11-19 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0005_alter_movie_review_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('mood_emoji', models.CharField(choices=[('emotions/angry.jpg', '분노'), ('emotions/calm.jpg', '평온'), ('emotions/excited.jpg', '신남'), ('emotions/happy.jpg', '행복'), ('emotions/sad.jpg', '슬픔'), ('emotions/sleepy.jpg', '지루')], max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('gpt_comment', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diaries', to=settings.AUTH_USER_MODEL)),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_diaries', to=settings.AUTH_USER_MODEL)),
                ('recommend_movie', models.ManyToManyField(blank=True, to='movies.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Diary_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('diary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='diaries.diary')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
