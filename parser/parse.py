from typing import OrderedDict, List, Any
from fake_useragent import UserAgent

import requests
from bs4 import BeautifulSoup
from PIL import Image


class Parser:
    ua = UserAgent()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    @staticmethod
    def write_html_to_file(soup: BeautifulSoup):
        with open('html.txt', 'w') as file:
            print(soup.prettify())
            # data = soup.
            # file.write(data)
    @staticmethod
    def parse_photo(url: str) -> Image:
        with requests.get(url, headers=Parser.headers, stream=True).raw as raw_image:
            return Image.open(raw_image)

    @staticmethod
    def parse_photos(soup: BeautifulSoup) -> list:
        img = []
        picture = soup.find_all('picture')
        for i in picture:
            image_code = i.find('img')
            img.append(Parser.parse_photo(image_code['src']))
        return img

    @staticmethod
    def parse_size(soup: BeautifulSoup) -> list[Any]:
        print(soup.prettify())
        # table = soup.find('fieldset', class_=" mt5-sm mb3-sm body-2 css-1pj6y87")
        # divs = table.findChildren('div', recursive=True)
        table = soup.find('div', class_='mt2-sm css-hzulvp')
        # for i in divs:
        #     print(i)
        print(table)
        sizes = []
        return sizes
    @staticmethod
    def parse_shoes(url: str) -> None:
        print(Parser.headers)
        with requests.get(url, headers=Parser.headers) as html_file:
            soup = BeautifulSoup(html_file.content, 'html.parser')
            name = soup.find(id='pdp_product_title').text
            gender = soup.find('h2', {'data-test': 'product-sub-title'}).text
            price_with_currency = soup.find('div', class_='is--current-price').text
            currency = price_with_currency[0]
            price = price_with_currency[1:]
            images = Parser.parse_photos(soup)
            size = Parser.parse_size(soup)
            # for i in size:
            #     print(i)
    @staticmethod
    def parse_by_link(url: str) -> None:
        with requests.get(url, headers=Parser.headers) as html_file:
            soup = BeautifulSoup(html_file.content, 'html.parser')
            products = soup.find_all("div", class_="product-card")
            a = soup.find('a', class_="product-card__link-overlay").get('href')
            print(a)


p = Parser()
# p.parse_by_link('https://www.adidas.com/us')
# p.parse_by_link('https://www.nike.com/w/new-mens-shoes-3n82yznik1zy7ok')
p.parse_shoes('https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700')
# p.parse_shoes('https://www.adidas.com/us/gazelle-shoes/IG0669.html')