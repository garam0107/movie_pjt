from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username


class User(AbstractUser):
    name = models.CharField(max_length=25)
    nickname = models.CharField(max_length=100)
    stone = models.IntegerField(default=0)
    profile_image = models.CharField(max_length=255, choices=[
    ('profile_images/profile1.jpg', 'profile 1'),
    ('profile_images/profile2.jpg', 'profile 2'),
    ('profile_images/profile3.jpg', 'profile 3'),
    ('profile_images/profile4.jpg', 'profile 4'),
    ('profile_images/profile5.jpg', 'profile 5'),
    ('profile_images/profile6.jpg', 'profile 6'),
], default='profile_images/default_profile.jpg')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    visit_count = models.IntegerField(default=0)
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        nickname = data.get("nickname")
        profile_image = data.get("profile_image")
        name = data.get("name")

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
        if name:
            user_field(user, "name", name)
            
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user