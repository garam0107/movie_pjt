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
    ('profile_images/profile1.jpg', 'profile 1'),
    ('profile_images/profile2.jpg', 'profile 2'),
    ('profile_images/profile3.jpg', 'profile 3'),
    ('profile_images/profile4.jpg', 'profile 4'),
    ('profile_images/profile5.jpg', 'profile 5'),
    ('profile_images/profile6.jpg', 'profile 6'),
        ],
        required=False,
        allow_blank=True
    )
    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()  # 기본 필드 가져오기
        cleaned_data['nickname'] = self.validated_data.get('nickname', '')  # nickname 추가
        cleaned_data['profile_image'] = self.validated_data.get('profile_image', '')
        return cleaned_data


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
    recommend_movie = UserMovieSerializer(source = 'diaries', many = True, read_only = True)
    followings_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'nickname', 'profile_image', 'visit_count'
                  'my_review','recommend_movie','followings','followers','followings_count','followers_count','stone']
        
    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()
    

class CustomUserDetailsSerializer(UserDetailsSerializer):
    # my_review = UserReviewSerializer(source='moviereview_set', many=True, read_only=True)
    # recommend_movie = UserMovieSerializer(source='diaries', many=True, read_only=True)
    followings_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
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
        if hasattr(UserModel, 'profile_image'):
            extra_fields.append('profile_image')    
        if hasattr(UserModel, 'visit_count'):
            extra_fields.append('visit_count')                
        model = UserModel
        fields = ['pk','followers_count','followings_count','stone', *extra_fields]
        read_only_fields = ('email',)

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()