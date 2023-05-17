import random
import uuid
from typing import Protocol, OrderedDict

from django.core.cache import cache
from templated_email import send_templated_mail

from src import settings
from users import repos
from .models import CustomUser


class UserServicesInterface(Protocol):
    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> CustomUser | None: ...

    def create_token(self, data: OrderedDict) -> dict: ...

    def verify_token(self, data: OrderedDict) -> dict: ...


class UserServicesV1:
    user_repos = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        session_id = self._verify_email(data=data)

    def verify_user(self, data: OrderedDict) -> CustomUser | None: ...

    def create_token(self, data: OrderedDict) -> dict: ...

    def verify_token(self, data: OrderedDict) -> dict: ...

    def _verify_email(self, data: OrderedDict, is_exists: bool = False) -> str:
        email = data['email']
        if is_exists:
            user = self.user_repos.get_user(data=data)
            email = str(user.email)

        code = self._generate_code()
        session_id = self._generate_session_id()

        cache.set(session_id, {'email': email, 'code': code, **data}, timeout=300)

        # TODO: Write send email code

        return session_id

    @staticmethod
    def _send_letter_to_email(user: CustomUser) -> None:
        send_templated_mail(
            template_name='Welcome',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            context={
                'email': user.email,
            },
        )

    # @staticmethod
    # def send_letter_to_email(mail: str, lname: str, fname: str) -> None:
    #     send_templated_mail(
    #         template_name='welcome',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[mail],
    #         context={
    #             'name': f'{fname, lname}',
    #             'email': mail,
    #         },
    #     )

    @staticmethod
    def _generate_code(length: int = 6) -> str:
        numbers = [str(i) for i in range(10)]
        return ''.join(random.choices(numbers, k=length))

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())
