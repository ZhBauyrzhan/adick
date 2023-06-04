import uuid
from typing import Protocol, OrderedDict

from templated_email import send_templated_mail

from src import settings
from users import repos
from .models import CustomUser
from django.db import transaction


class UserServiceInterface(Protocol):
    def create_user(self, data: OrderedDict, **kwargs) -> CustomUser: ...

    def get_user_by_id(self, user_id: uuid.UUID) -> CustomUser: ...

    def get_user_by_username(self, username: str) -> CustomUser: ...

    def get_user_by_email(self, email: str) -> CustomUser: ...

    def get_all_users(self) -> list[CustomUser]: ...

    def update_user(self, user_id: uuid.UUID, **update_fields) -> CustomUser: ...

    def delete_user(self, user_id: uuid.UUID) -> bool: ...


class UserServiceV1:
    user_repos = repos.UserReposV1()

    def get_user_by_id(self, user_id: uuid.UUID) -> CustomUser:
        return self.user_repos.get_user_by_id(user_id=user_id)

    def get_user_by_username(self, username: str) -> CustomUser:
        return self.user_repos.get_user_by_username(username)

    def get_user_by_email(self, email: str) -> CustomUser:
        return self.user_repos.get_user_by_email(email)

    def get_all_users(self) -> list[CustomUser]:
        return self.user_repos.get_all_users()

    @transaction.atomic()
    def create_user(self, data: OrderedDict) -> CustomUser:
        user = self.user_repos.create_user(data)
        self._send_letter_to_email(user=user, template_name='welcome')
        return user

    def update_user(self, user_id: uuid.UUID, **update_fields) -> CustomUser:
        return self.user_repos.update_user(user_id, update_fields)

    @transaction.atomic()
    def delete_user(self, user: CustomUser) -> bool:
        self._send_letter_to_email(user, template_name='delete')
        res = self.user_repos.delete_user(user.id)
        return res

    @staticmethod
    def _send_letter_to_email(user: CustomUser, template_name: str) -> None:
        context = {}
        match template_name:
            case 'welcome':
                context = {'username': user.username}
            case 'delete':
                context = {'username': user.username}
        send_templated_mail(
            template_name=template_name,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            context=context,
        )
