from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from . import services, serializers


class UserViewSet(ViewSet):
    user_services: services.UserServicesInterface = services.UserServicesV1()

    def create_user(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.user_services.create_user(data=serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)

    def verify_user(self, request, *args, **kwargs):
        serializer = serializers.VerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.user_services.verify_user(data=serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def create_token(self, request, *args, **kwargs):
        serializer = serializers.CreateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = self.user_services.create_token(data=serializer.validated_data)
        return Response(session_id, status=status.HTTP_201_CREATED)
    def verify_token(self, request, *args, **kwargs):
        serializer = serializers.VerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = self.user_services.verify_token(data=serializer.validated_data)
        return Response(tokens, status=status.HTTP_200_OK)