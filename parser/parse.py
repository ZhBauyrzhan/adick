from PIL import Image
import requests
from _decimal import Decimal

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time


class Parser:
    """Нужно переписать получение chrome driver-а"""
    serv = Service('C:/Program Files (x86)/chromedriver.exe')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    @staticmethod
    def parse_size(driver: Chrome, xpath: str) -> list[Decimal]:
        container = driver.find_element(by=By.XPATH, value=xpath)
        divs = driver.find_elements(by=By.TAG_NAME, value='div')
        sizes: list[Decimal] = []
        for div in divs:
            size = Decimal(div.find_element(by=By.TAG_NAME, value='label').text)
            disabled = div.find_element(by=By.TAG_NAME, value='input').get_attribute('disabled')
            if disabled is None:
                sizes.append(size)
        return sizes
    @staticmethod
    def parse_photo(url: str) -> Image:
        with requests.get(url, headers=Parser.headers, stream=True).raw as raw_image:
            return Image.open(raw_image)

    @staticmethod
    def parse_photos(driver: Chrome, xpath: str) -> list[Image]:
        photos = driver.find_element(by=By.XPATH, value=xpath)
        img = photos.find_elements(by=By.TAG_NAME, value='img')
        images = []
        for i in img:
            image=Parser.parse_photo(i.get_attribute('src'))
            images.append(image)
            # image.show()
        return images

    @staticmethod
    def parse_shoes(url: str, xpath_photos: str, xpath_size: str) -> None:
        opts = ChromeOptions()
        # opts.headless = True
        driver = Chrome(service=Parser.serv, options=opts)
        driver.get(url)
        driver.maximize_window()
        # images = Parser.parse_photos(driver=driver, xpath=xpath_photos)
        sizes = Parser.parse_size(driver=driver, xpath=xpath_size)
        print(sizes)
p = Parser()
xpath_photos = {
    'nike': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[1]"""
}
# p.parse_photos(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700', xpath=xpath_photos['nike'])
xpath_size = {
    'nike': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div"""
}
# print(Decimal( '6.5' ))
# p.parse_shoes(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700',
#               xpath_photos=xpath_photos['nike'], xpath_size=xpath_size['nike'])