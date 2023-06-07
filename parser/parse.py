import uuid
from _decimal import Decimal
from io import BytesIO

from PIL import Image
import requests
from celery import shared_task
from django.core.files.base import ContentFile
from rest_framework.generics import get_object_or_404
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from parser.models import Item, ItemPhoto, ItemSize, Shop
from django.db import transaction


class Parser:
    serv = Service('/usr/bin/chromedriver')

    @staticmethod
    def _parse_size(driver: Chrome, xpath: str) -> list[str]:
        # time.sleep(10)
        # time.sleep(5)
        fieldset = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))

        # print(fieldset.text)
        # time.sleep(1000)
        text: str = fieldset.text
        return text.split('\n')

    @staticmethod
    def _parse_photo(url: str) -> Image:
        # print(f'!!!!!!URL = {url}')
        with requests.get(url, stream=True).raw as raw_image:
            return Image.open(raw_image)

    @staticmethod
    def _parse_photos(driver: Chrome, xpath: str) -> list[Image]:
        # print('WAS')
        container = driver.find_element(by=By.XPATH, value=xpath)
        # print(container.text)
        photos = container.find_elements(by=By.TAG_NAME, value='img')

        images = []
        for i in photos:
            url = i.get_attribute('src')
            if url is not None and url.startswith('https://static.nike.com/'):
                images.append(Parser._parse_photo(url))
        return images

    @staticmethod
    def _cookies(driver: Chrome, xpath: str) -> None:
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            time.sleep(2)
            button.click()
        except Exception as e:
            print('No need to work with cookies')

    @staticmethod
    def _parse_name(driver: Chrome, xpath: str) -> str:
        name = driver.find_element(by=By.XPATH, value=xpath).text
        return name

    @staticmethod
    def _parse_price(driver: Chrome, xpath: str) -> str:
        price = driver.find_element(by=By.XPATH, value=xpath).text
        return price

    @staticmethod
    def _country(driver: Chrome, xpath: str) -> None:
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            time.sleep(2)
            button.click()
        except Exception as e:
            print('No need to work with country')

    @staticmethod
    @transaction.atomic
    def _save_item(url: str, title: str, currency: str, price: Decimal,
                   images: list, sizes: list[str], shop: Shop):
        item = Item(title=title, price=price, currency=currency, shop=shop, url=url)
        item.save()
        validated_sizes = Parser._validate_sizes(sizes)
        item.size.add(*validated_sizes)

        for i in images:
            image = ItemPhoto(item=item, is_main=(i == images[0]))
            image_buffer = BytesIO()
            i.save(image_buffer, format='PNG')
            name = str(uuid.uuid4()) + '.png'
            image.photo.save(name, ContentFile(image_buffer.getvalue()), save=True)
            image.save()

    @staticmethod
    def parse_items(url: str, xpath: dict, shop: Shop) -> None:

        with Parser.setup_driver(url) as driver:
            try:
                Parser._country(driver=driver, xpath=xpath['country'])
                Parser._cookies(driver=driver, xpath=xpath['accept'])
                time.sleep(20)
                title = Parser._parse_name(driver=driver, xpath=xpath['name'])
                print(title)
                price_with_currency = Parser._parse_price(driver=driver, xpath=xpath['price'])
                print(price_with_currency)
                currency = price_with_currency[0]
                price = Decimal(price_with_currency[1:])
                sizes = []
                try:
                    sizes = Parser._parse_size(driver=driver, xpath=xpath['size'])
                except Exception as e:
                    print('No size 1')
                if len(sizes) == 0:
                    try:
                        sizes = Parser._parse_size(driver=driver, xpath=xpath['size2'])
                    except Exception as e:
                        print('No size 2')
                print(sizes)
                images = Parser._parse_photos(driver=driver, xpath=xpath['photos'])
                print(len(images))
                # try:
                #     for i in images:
                #         i.show()
                # except Exception as e:
                #     print(e)
                Parser._save_item(url, title, currency, price, images, sizes, shop)
            except Exception as e:
                print(e, url)
    @staticmethod
    def _validate_sizes(sizes):
        validated_sizes = []
        for i in sizes:
            if not ItemSize.objects.filter(size=i).exists():
                item_size = ItemSize(size=i)
                item_size.save()
                validated_sizes.append(item_size.id)
            else:
                item_size = ItemSize.objects.filter(size=i).first()
                validated_sizes.append(item_size.id)
        return validated_sizes


    @staticmethod
    def _get_grid_links(url: str, xpath: dict) -> list:
        '''Тут я изменил в бд цену на 200, а потом проверил, что если он спарсит эти же кросы, то цену поменяет'''
        # return [ (
        #     'https://www.nike.com/t/air-force-1-07-mens-shoes-jBrhbr/CW2288-111',
        #     Decimal(100),
        #     '$'
        # ), ]
        with Parser.setup_driver(url) as driver:
            screen_height = screen_height = driver.execute_script("return window.screen.height;")

            Parser._country(driver=driver, xpath=xpath['country2'])
            Parser._cookies(driver=driver, xpath=xpath['accept2'])
            time.sleep(25)
            # print(screen_height)
            items = []
            # TODO: change for -> while when run in sever
            for i in range(1, 2):
                Parser.scroll_page(driver, screen_height, i)
                divs = driver.find_elements(by=By.CLASS_NAME, value='product-card')
                for i in divs:
                    text = i.text.split('\n')
                    price_with_currency = text[-1]
                    price = Decimal(price_with_currency[1:])
                    currency = price_with_currency[0]

                    link = i.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                    items.append(
                        (
                            link,
                            price,
                            currency
                        )
                    )
                    # print(link.get_attribute('href'))
                time.sleep(5)
            items = list(set(items))
            return items

    @staticmethod
    def parse_item_grid(url: str, xpath: dict, shop: Shop):
        # shop = get_object_or_404(Shop, name=shop_name)

        items = Parser._get_grid_links(url, xpath)
        # print(links)
        # cnt = 0
        for item in items:
            item_url = item[0]
            print(item_url)
            price = item[1]
            currency = item[2]
            if not Item.objects.filter(url=item_url).exists():
                Parser.parse_items(url=item_url, xpath=xpath, shop=shop)
            elif Item.objects.get(url=item_url).price.compare(price) != 0 and Item.objects.get(url=item_url).currency == currency:
                item_db = Item.objects.get(url=item_url)
                item_db.price = price
                item_db.save()
            # if cnt == 1:
            #     break
            # cnt += 1
    @staticmethod
    def scroll_page(driver: Chrome, screen_height, i):
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))

    @staticmethod
    def setup_driver(url: str) -> Chrome:
        opts = ChromeOptions()
        # opts.headless = True
        driver = Chrome(service=Parser.serv, options=opts)
        driver.get(url)
        driver.maximize_window()
        return driver

# p = Parser()
#
# xpath_nike = {
#     'photos': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[2]""",
#     'size': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div""",
#     'accept': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]""",
#     'decline': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[2]""",
#     'name': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h1""",
#     'price': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div
#     /div[2]/div/div/div/div/div""",
#     'country': """/html/body/div[6]/div/div/nav/button""",
#     'grid': """/html/body/div[4]/div/div/div[2]/div[4]/div/div[5]/div[2]""",
#     'accept2': """/html/body/div[6]/div/div/div/div/div/section/div[2]/div/button[1]""",
#     'country2': """/html/body/div[5]/div/div/nav/button""",
# }

# p.parse_shoes(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700', xpath=xpath_nike)

# p.parse_items(url='https://www.nike.com/t/air-zoom-flight-95-mens-shoes-zc42bP/DX5505-100', xpath=xpath_nike)

# links = p.parse_item_grid(url='https://www.nike.com/w/mens-shoes-nik1zy7ok', xpath=xpath_nike)
# for link in links:
#     p.parse_items()

# photo 1 /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[2]

# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div
# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div/div[1]
# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div/div[17]

# name /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h1

# price /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div

# star /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[4]/div/details[2]/summary/div
# aria-label="4.8"
#        /html/body/div[6]/div/div/div/div/div/section/div[2]/div/button[1]
# accept /html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]
# decline /html/body/div[7]/div/div/div/div/div/section/div[2]/div/butt on[2]
