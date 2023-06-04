from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ViewSet, ModelViewSet
from . import services, serializers


class UserViewSet(ViewSet):
    user_service = services.UserServiceV1()

    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.user_service.create_user(data=serializer.validated_data)
        response_serializer = serializers.UserSerializer(queryset)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.user_service.get_all_users()
        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        queryset = self.user_service.get_user_by_username(kwargs.get('username'))
        serializer = serializers.UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.user_service.get_user_by_username(kwargs.get('username'))
        res = self.user_service.delete_user(user)
        return Response(res, status=status.HTTP_200_OK)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'get' or self.action == 'update' \
                or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser, IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
