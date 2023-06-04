import uuid
from typing import Protocol, OrderedDict
from rest_framework.generics import get_object_or_404

from .models import CustomUser


class UserReposInterface(Protocol):
    def create_user(self, data: OrderedDict, **kwargs) -> CustomUser: ...

    def get_user_by_id(self, user_id: uuid.UUID) -> CustomUser: ...

    def get_user_by_username(self, username: str) -> CustomUser: ...

    def get_user_by_email(self, email: str) -> CustomUser: ...

    def get_all_users(self) -> list[CustomUser]: ...

    def update_user(self, user_id: uuid.UUID, **update_fields) -> CustomUser: ...

    def delete_user(self, user_id: uuid.UUID) -> bool: ...


class UserReposV1:
    model = CustomUser

    def get_user_by_id(self, user_id: uuid.UUID) -> CustomUser:
        return get_object_or_404(self.model, id=user_id)

    def get_user_by_username(self, username: str) -> CustomUser:
        return get_object_or_404(self.model, username=username)

    def get_user_by_email(self, email: str) -> CustomUser:
        return get_object_or_404(self.model, email=email)

    def get_all_users(self) -> list[CustomUser]:
        return list(self.model.objects.all())

    def create_user(self, data: OrderedDict) -> CustomUser:
        print(data)
        user = self.model.objects.create_user(**data)
        return user

    def update_user(self, user_id: uuid.UUID, **update_fields) -> CustomUser:
        user = get_object_or_404(self.model, id=user_id)
        for key, value in update_fields.items():
            setattr(user, key, value)
        user.save()
        return user

    def delete_user(self, user_id: uuid.UUID) -> bool:
        user = get_object_or_404(self.model, id=user_id)
        user.delete()
        return True
