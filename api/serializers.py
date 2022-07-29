from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *
from app.models import Device

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


class RegisterDeviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Device
        fields = ("name", "tag", "key")
        extra_kwargs = {
            "key": {
                "validators": []
            }
        }

    def create(self, validated_data):
        device = Device.objects.create(
            name=validated_data.get("name", None),
            tag=validated_data.get("tag", None),
            owner=validated_data.get('owner')
        )
        return device


