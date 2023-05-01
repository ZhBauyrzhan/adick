from django.db import models
from .choices import GenderChoice, CurrencyChoice
from django.utils.translation import gettext_lazy as _
from forex_python.converter import CurrencyRates

# Create your models here.
class Shoes(models.Model):
    title = models.CharField(max_length=60, verbose_name=_('Title'))
    gender = models.CharField(max_length=10, choices=GenderChoice.choices, verbose_name=_('Gender'))
    price = models.DecimalField(verbose_name=_('Price'))
    currency = models.CharField(max_length=3, choices=CurrencyChoice.choices, verbose_name=_('Currency'))

    class Meta:
        verbose_name = _('Shoes')
        verbose_name_plural = _('Shoes')
