from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    @staticmethod
    def _check_fields(email: models.EmailField,
                      username: models.CharField,
                      password: models.CharField) -> bool:
        if not email or not username or not password:
            return False
        return True

    def create_user(self, email: models.EmailField,
                    username: models.CharField,
                    password: models.CharField):
        if not CustomUserManager._check_fields(email, username, password):
            raise ValueError('Check fields values')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: models.EmailField,
                         username: models.CharField,
                         password: models.CharField):

        if not CustomUserManager._check_fields(email, username, password):
            raise ValueError('Check fields values')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user

    def active(self):
        return self.filter(is_active=True)