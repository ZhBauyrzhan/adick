from src.celery import app
from users.models import UserItems
from .parse import Parser
from .models import Shop, ShopXPATH, Item


@app.task
def start_parser(*args, **kwargs):
    shops = Shop.objects.all()
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
            'country2': shop_xpath.country_2
        }
        Parser.parse_item_grid(url, xpath, shop)

@app.task
def send_emails(*args, **kwargs):
    #TODO
    # items = UserItems.objects.filter(last_price__exact=)
    ...