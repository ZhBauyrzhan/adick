from src.celery import app
from users.models import UserItems, CustomUser
from .parse import Parser
from .models import Shop, ShopXPATH, Item
from django.db.models import Q, F


@app.task
def start_parser(*args, **kwargs):
    shops = Shop.objects.all()
    print(shops)
    for shop in shops:
        url = shop.url
        shop_xpath = shop.xpath
        # print(shop_xpath)
        xpath = {
            'photos': shop_xpath.photos,
            'size': shop_xpath.size,
            'accept': shop_xpath.cookies_accept,
            'decline': shop_xpath.cookies_decline,
            'name': shop_xpath.item_name,
            'price': shop_xpath.price,
            'country': shop_xpath.country,
            'grid': shop_xpath.grid,
            'accept2': shop_xpath.cookies_accept_2,
            'country2': shop_xpath.country_2,
            'size2': shop_xpath.size_2
        }
        print(xpath, url)
        Parser.parse_item_grid(url, xpath, shop)


@app.task
def send_emails(*args, **kwargs):
    user_items = UserItems.objects.exclude(item__price__exact=F('last_price')).prefetch_related('users')

    # TODO
    # items = UserItems.objects.filter(last_price__exact=)
    ...
