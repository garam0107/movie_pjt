from django.shortcuts import render, get_list_or_404, get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
# Create your views here.

def user_diary(request, user_pk):
    pass