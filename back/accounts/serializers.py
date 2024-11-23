from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.registration.serializers import RegisterSerializer



from diaries.models import Diary
from movies.models import Movie_review

UserModel = get_user_model()


# 회원가입시 필요한 정보 추가
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
    name = serializers.CharField(
        required = False,
        allow_blank = True,
        max_length = 25
    )
    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()  # 기본 필드 가져오기
        cleaned_data['nickname'] = self.validated_data.get('nickname', '')  # nickname 추가
        cleaned_data['profile_image'] = self.validated_data.get('profile_image', '')
        cleaned_data['name'] = self.validated_data.get('name', '')
        return cleaned_data

# 유저가 팔로우 한 사람들의 일기
class UserFollowingDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id','author', 'title', 'content']

# 유저가 팔로우 한 사람들의 영화 리뷰
class UserFollowingReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source = 'movie.title', read_only = True)
    poster_path = serializers.CharField(source = 'movie.poster_path', read_only = True)
    review_user_id = serializers.CharField(source = 'user.username', read_only = True)
    profile_image = serializers.CharField(source = 'user.profile_image', read_only = True)
    class Meta:
        model = Movie_review
        fields= ['id','movie', 'title', 'content','movie_title','poster_path','review_user_id','rating','profile_image']


# 유저가 챗봇에 추천 받은 영화들
class UserMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['recommend_movie']
class UserReasonSerializer(serializers.ModelSerializer):
     class Meta:
        model = Diary
        fields = ['recommend_reasons']

# 유저의 영화 리뷰들
class UserReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source = 'movie.title', read_only = True)
    movie_poster_path = serializers.CharField(source = 'movie.poster_path', read_only = True)
    movie_id = serializers.CharField(source = 'movie.id', read_only = True)
    class Meta:
        model = Movie_review
        fields= ['title', 'content','movie_title','rating','created_at','movie_poster_path','movie_id']
        
# 유저 정보
class UserSerializer(serializers.ModelSerializer):
    my_review = UserReviewSerializer(source = 'reviews', many = True, read_only = True)
    recommend_movie = UserMovieSerializer(source = 'diaries', many = True, read_only = True)
    followings_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    recommend_reasons = UserReasonSerializer(source = 'diaries', many = True, read_only = True)
    class RecommendMovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Diary
            fields = ['recommend_movie_titles']
    movies_titles = RecommendMovieSerializer(source='diaries', many=True, read_only=True)  
    class Meta:
        model = UserModel
        fields = ['id','name', 'username', 'email', 'first_name', 'last_name', 'nickname', 'profile_image', 'visit_count',
                  'my_review','recommend_movie','recommend_reasons','followings','followers','followings_count','followers_count','stone','movies_titles']
        
    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()
    
    
# 유저 정보 가져오기
class CustomUserDetailsSerializer(UserDetailsSerializer):
    my_review = UserReviewSerializer(source='moviereview_set', many=True, read_only=True)
    recommend_movie = UserMovieSerializer(source='diaries', many=True, read_only=True)
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
        fields = ['pk','followers_count','followings_count','stone','my_review','recommend_movie','name', *extra_fields]
        read_only_fields = ('email',)

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()
    
# 유저 정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['profile_image', 'nickname']

# 모든 유저 정보 들고오기
class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'stone', 'nickname']

