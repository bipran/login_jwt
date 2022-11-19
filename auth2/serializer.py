from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        user =User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user 
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs={
            "password":{"write_only":True},
        }

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","password")