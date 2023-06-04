import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from . import managers


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    email = models.EmailField(unique=True, verbose_name=_("Email"))
    username = models.CharField(unique=False,max_length=25, verbose_name=_('Username'))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'password']

    objects = managers.CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.email=} {self.username=}"