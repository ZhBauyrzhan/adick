from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'email']

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class UserItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserItems
        fields = '__all__'