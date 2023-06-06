from rest_framework import serializers
from . import models


class ShopXPATHSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopXPATH
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    # xpath = ShopXPATHSerializer()

    class Meta:
        model = models.Shop
        fields = '__all__'


class ParserSerializer(serializers.Serializer):
    url = serializers.URLField()
    shop = serializers.CharField()
