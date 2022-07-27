from django.contrib.auth.hashers import make_password
from django.forms import CharField
from rest_framework import serializers, generics
from .models import *
from rest_framework.response import Response


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("password", "username", "first_name", "last_name", "email")
        # extra_kwargs = {'first_name': {'required': False}, 'last_name': {'required': False}}


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get("username"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email"),
            password=make_password(validated_data.get("password")),
        )
        return user

class AgainVerifySerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
