from src.celery import app
from .parse import Parser
from .models import Shop, ShopXPATH


@app.task
def start_parser(url: str, shop_name: str, *args, **kwargs):
    shop = Shop.objects.get(name__exact=shop_name)
    shop_xpath = shop.xpath
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
        'country2': shop_xpath.country_2
    }
    Parser.parse_item_grid(url, xpath, shop)
