from django.http import HttpRequest
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import *
from api.models import User
from api.serializers import RegisterUserSerializer
from rest_framework import serializers
from django.db import transaction
from rest_framework.response import Response
from django.conf import settings
import jwt
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

@transaction.atomic
def Register_services(request: HttpRequest, serializer_class: RegisterUserSerializer):
    
    serializer = _base_ser_settings(request=request, serializer_class=serializer_class)
    serializer.save()
    absurl = _generator_absurl(username=serializer.data["username"], request=request)

    Util.send_email(
        username=serializer.data["username"],
        absurl=absurl,
        email=serializer.data["email"]
    )

def VerifiEmail_services(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    user = User.objects.get(username=payload["user_id"])

    Token.objects.create(user=user)
    user.is_verified = True
    user.save()


def AgainVerifyEmail_services(request: HttpRequest, serializer_class: RegisterUserSerializer): 
    serializer = _base_ser_settings(request, serializer_class)
    user = authenticate(**serializer.validated_data)

    if user is None:
        return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    usertoken = Token.objects.filter(user=user)

    if usertoken.exists():
        return Response({"error": "You are already verified"}, status=status.HTTP_400_BAD_REQUEST)
    
    absurl = _generator_absurl(request, user.username)

    Util.send_email(
        username=user.username, 
        absurl=absurl, 
        email=user.email
    )
    return Response({"message": "Ok"})


def _generator_absurl(request: HttpRequest, username: str) -> str:
    user = User.objects.get(username=username)
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request)
    relativLink = reverse('email-verify')

    return f"http://{current_site}{relativLink}?token={token}"


def _base_ser_settings(request: HttpRequest, serializer_class: serializers.ModelSerializer) -> serializers.ModelSerializer:
    data = request.data
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer
