from django.shortcuts import render
from dj_rest_auth.models import TokenModel
from rest_framework.generics import CreateAPIView
from dj_rest_auth.app_settings import api_settings
# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = api_settings.REGISTER_SERIALIZER
    permission_classes = api_settings.REGISTER_PERMISSION_CLASSES
    token_model = TokenModel
    throttle_scope = 'dj_rest_auth'
