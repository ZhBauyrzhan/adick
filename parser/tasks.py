from collections import defaultdict

from templated_email import send_templated_mail

from src import settings
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
    changed_user_items = UserItems.objects.filter(item__is_changed=True).select_related('user', 'item')
    items_by_email = defaultdict(list)

    for user_item in changed_user_items:
        user = user_item.user
        item = user_item.item
        items_by_email[user.email].append(
            {
                "Title": item.title,
                "new price": f'{item.currency}{item.price}'
            }
        )
        item.is_changed = False
        item.save()
    for email, items in items_by_email.items():
        text = [f'{i["Title"]} {i["new price"]}' for i in items]
        text = "\n".join(text)
        print(email)
        send_templated_mail(
            template_name="price-update",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            context={"text": text},
        )
        print(text)
