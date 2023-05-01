from typing import OrderedDict

import requests
from bs4 import BeautifulSoup
from PIL import Image


class Parser:
    @staticmethod
    def parse_photo(url: str) -> Image:
        with requests.get(url, stream=True).raw as raw_image:
            return Image.open(raw_image)

    @staticmethod
    def parse_photos(soup: BeautifulSoup) -> list:
        buttons = soup.find_all('div', class_='css-du206p') 
        # container = soup.find('div', id='pdp-6-up')
        # buttons = container.find_all('button', {"data-sub-type": "image"})
        for i in buttons:
            print(i)
             # pictures = i.find_all('img')
             # print(pictures)
        img = []
        return img

    @staticmethod
    def parse_size(soup: BeautifulSoup) -> dict:
        ...

    @staticmethod
    def parse_shoes(url: str) -> None:
        with requests.get(url) as html_file:
            soup = BeautifulSoup(html_file.content, 'html.parser')
            name = soup.find(id='pdp_product_title').text
            gender = soup.find('h2', {'data-test': 'product-sub-title'}).text
            price_with_currency = soup.find('div', class_='is--current-price').text
            currency = price_with_currency[0]
            price = price_with_currency[1:]
            images = Parser.parse_photos(soup)
            for i in images:
                i.show()

    @staticmethod
    def parse_by_link(url: str) -> None:
        with requests.get(url) as html_file:
            soup = BeautifulSoup(html_file.content, 'html.parser')
            products = soup.find_all("div", class_="product-card")
            a = soup.find('a', class_="product-card__link-overlay").get('href')

            print(a)


p = Parser()
# p.parse_by_link('https://www.nike.com/w/new-mens-shoes-3n82yznik1zy7ok')
p.parse_shoes('https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700')
