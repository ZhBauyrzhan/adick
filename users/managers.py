from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    @staticmethod
    def _check_fields_for_admin(email: models.EmailField,
                                first_name: models.CharField,
                                last_name: models.CharField,
                                ) -> bool:
        if not email or not first_name or not last_name:
            return False
        return True

    @staticmethod
    def _check_fields(email: models.EmailField,
                      first_name: models.CharField,
                      last_name: models.CharField) -> bool:
        if not email or not first_name or not last_name:
            return False
        return True

    def create_user(self, email: models.EmailField,
                    first_name: models.CharField,
                    last_name: models.CharField
                    ):
        if not CustomUserManager._check_fields(email, first_name, last_name):
            raise ValueError('Check fields values')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email: models.EmailField,
                         first_name: models.CharField,
                         last_name: models.CharField,
                         password: str):

        if not CustomUserManager._check_fields_for_admin(email, first_name, last_name):
            raise ValueError('Check fields values')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        return user

    def active(self):
        return self.filter(is_active=True)
