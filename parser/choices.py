from django.utils.translation import gettext_lazy as _
from django.db import models


class GenderChoice(models.TextChoices):
    MALE = _('Male')
    FEMALE = _('Female')


class ShopChoice(models.TextChoices):
    NIKE = _('nike')
    PUMA = _('puma')


class CurrencyChoice(models.TextChoices):
    USD = _('$'), _('USD')
    KZT = _('₸'), _('KZT')
    GBP = _('£'), _('GBP')
