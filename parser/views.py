from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet, ModelViewSet
from . import serializers
from .parse import Parser
from .models import Shop, ShopXPATH

from rest_framework.generics import get_object_or_404


class ShopView(ModelViewSet):
    serializer_class = serializers.ShopSerializer
    queryset = Shop.objects.all()
    permission_classes = IsAdminUser,


class ShopXPATH(ModelViewSet):
    serializer_class = serializers.ShopXPATHSerializer
    queryset = ShopXPATH.objects.all()
    permission_classes = IsAdminUser,


class ParserView(ViewSet):
    parser = Parser()

    xpath_nike = {
        'photos': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div""",
        'size': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div""",
        'accept': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]""",
        'decline': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[2]""",
        'name': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h1""",
        'price': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div
        /div[2]/div/div/div/div/div""",
        'country': """/html/body/div[6]/div/div/nav/button""",
        'grid': """/html/body/div[4]/div/div/div[2]/div[4]/div/div[5]/div[2]""",
        'accept2': """/html/body/div[6]/div/div/div/div/div/section/div[2]/div/button[1]""",
        'country2': """/html/body/div[5]/div/div/nav/button""",
    }

    def parse_item(self, request, *args, **kwargs):
        serializer = serializers.ParserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        shop_name = serializer.validated_data['shop']

        shop = get_object_or_404(Shop, name=shop_name)

        self.parser.parse_items(url, xpath=self.xpath_nike, shop=shop)
        return Response(status=status.HTTP_200_OK)

    def parse_grid(self, request, *args, **kwargs):
        serializer = serializers.ParserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        shop_name = serializer.validated_data['shop']

        shop = get_object_or_404(Shop, name=shop_name)

        self.parser.parse_item_grid(url, xpath=self.xpath_nike, shop=shop)
        return Response(status=status.HTTP_200_OK)
    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'parse_grid' or self.action == 'parse_item':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]
