from typing import Protocol, OrderedDict
from rest_framework.generics import get_object_or_404

from .models import User


class UserReposInterface(Protocol):
    def create_user(self, data: OrderedDict) -> User: ...

    def get_user(self, data: OrderedDict) -> User: ...

    # def get_users(self) -> list[User]: ...
    #
    # def update_user(self, data: OrderedDict) -> User: ...
    #
    # def delete_user(self, data: OrderedDict) -> None: ...


class UserReposV1:
    model = User

    def create_user(self, data: OrderedDict) -> User:
        return self.model.objects.create_user(**data)

    def get_user(self, data: OrderedDict) -> User:
        return get_object_or_404(self.model, **data)
