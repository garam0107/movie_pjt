from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.registration.serializers import RegisterSerializer


from .models import User
from diaries.models import Diary
from movies.models import Movie_review

UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
      required=False,
      allow_blank=True,
      max_length=255
    )
    profile_image = serializers.ChoiceField(
        choices=[
            ('profile_images/character_single1.jpg', 'Image 1'),
            ('profile_images/character_single2.jpg', 'Image 2'),
            ('profile_images/character_single3.jpg', 'Image 3'),
            ('profile_images/character_single4.jpg', 'Image 4'),
            ('profile_images/character_single5.jpg', 'Image 5'),
            ('profile_images/character_single6.jpg', 'Image 6'),
        ],
        required=False,
        allow_blank=True
    )
    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()  # 기본 필드 가져오기
        cleaned_data['nickname'] = self.validated_data.get('nickname', '')  # nickname 추가
        cleaned_data['profile_image'] = self.validated_data.get('profile_image', '')
        return cleaned_data
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')    
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)

class UserFollowingDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id','autor', 'title', 'content']


class UserFollowingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_review
        fields= ['id','movie', 'title', 'content']



class UserMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['recommend_movie']

class UserReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source = 'movie.title', read_only = True)
    class Meta:
        model = Movie_review
        fields= ['title', 'content','movie_title']

class UserSerializer(serializers.ModelSerializer):
    my_review = UserReviewSerializer(source = 'moviereview_set', many = True, read_only = True)
    recommed_movie = UserMovieSerializer(source = 'diaries', many = True, read_only = True)
    class Meta:
        model = User
        fields = '__all__'