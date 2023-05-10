from django.db import models
from .choices import ShopChoice
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=60, verbose_name=_('Title'))
    price = models.DecimalField(verbose_name=_('Price'), max_digits=9, decimal_places=2)

    shop = models.ForeignKey(to='Shop', verbose_name=_('Shop'), on_delete=models.PROTECT)

    url = models.TextField(verbose_name=_('URL'))

    size = models.ForeignKey(to='ItemSize', on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Shoes')
        verbose_name_plural = _('Shoes')


class Shop(models.Model):
    name = models.CharField(max_length=60, verbose_name=_('Shop name'), choices=ShopChoice.choices)
    url = models.TextField(verbose_name=_('URL'))


class ShopXPATH(models.Model):
    shop = models.OneToOneField(to='Shop', on_delete=models.CASCADE)
    photos: models.TextField(verbose_name=_('Photo'))
    size: models.TextField(verbose_name=_('Size'))
    cookies_accept: models.TextField(verbose_name=_('Accept cookies'))
    cookies_decline: models.TextField(verbose_name=_('Decline cookies'))
    item_name: models.TextField(verbose_name=_('Item name'))
    price: models.TextField(verbose_name=_('Price'))
    country: models.TextField(verbose_name=_('Country'))


class ItemSize(models.Model):
    size = models.CharField(max_length=20, verbose_name=_('Size'))


class ItemPhoto(models.Model):
    photo = models.ImageField(verbose_name=_('Item image'), null=True, blank=True)
    item = models.ForeignKey(to='Item', verbose_name=_('Item'), related_name=_('item'), on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name=_('Is main photo?'), default=False)
