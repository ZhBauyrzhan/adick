import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from . import managers


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    email = models.EmailField(unique=True, verbose_name=_("Email"))
    first_name = models.CharField(max_length=40, verbose_name=_("First name"))
    last_name = models.CharField(max_length=40, verbose_name=_("Last name"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created time"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated time"))

    USERNAME_FIELD = "email"
    objects = managers.CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name} {self.gender}"

    def __str__(self):
        return f"{self.email=}"
