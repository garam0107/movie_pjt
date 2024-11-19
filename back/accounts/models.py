from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username


class User(AbstractUser):
    nickname = models.CharField(max_length=100)
    stone = models.IntegerField(null=True)
    profile_image = models.CharField(max_length=255, choices=[
    ('profile_images/character_single1.jpg', 'Image 1'),
    ('profile_images/character_single2.jpg', 'Image 2'),
    ('profile_images/character_single3.jpg', 'Image 3'),
    ('profile_images/character_single4.jpg', 'Image 4'),
    ('profile_images/character_single5.jpg', 'Image 5'),
    ('profile_images/character_single6.jpg', 'Image 6'),
], default='profile_images/image1.jpg')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        nickname = data.get("nickname")
        profile_image = data.get("profile_image")


        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if profile_image:
            user_field(user, "profile_image", profile_image)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user