from django.shortcuts import render
from dj_rest_auth.models import TokenModel
from rest_framework.generics import CreateAPIView
from dj_rest_auth.app_settings import api_settings

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render,get_list_or_404,get_object_or_404
# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = api_settings.REGISTER_SERIALIZER
    permission_classes = api_settings.REGISTER_PERMISSION_CLASSES
    token_model = TokenModel
    throttle_scope = 'dj_rest_auth'

@api_view(['GET','POST','DELETE','PUT'])
def mypage(request, user_pk):
    pass