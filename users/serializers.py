from rest_framework import serializers
from . import models


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = '__all__'


class VerifyUserSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    code = serializers.CharField(max_length=6)


class CreateTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()


class GetUserSerializer(serializers.Serializer):
    token = serializers.CharField()