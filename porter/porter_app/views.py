from django.shortcuts import render
from django.http import HttpResponse
from .models import Driver,user,MyUser,Admin
# Create your views here.
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserSignupSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response


def index():
    return HttpResponse("welcome to porter")
