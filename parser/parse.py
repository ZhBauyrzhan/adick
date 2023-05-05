from PIL import Image
import requests

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time


class Parser:
    """Нужно переписать получение chrome driver-а"""
    serv = Service('C:/Program Files (x86)/chromedriver.exe')
    opts = ChromeOptions()
    # opts.headless = True
    driver = Chrome(service=serv, options=opts)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

    @staticmethod
    def parse_photo(url: str) -> Image:
        with requests.get(url, headers=Parser.headers, stream=True).raw as raw_image:
            return Image.open(raw_image)

    @staticmethod
    def parse_photos(url: str, xpath: str) -> list[Image]:
        Parser.driver.get(url)
        Parser.driver.maximize_window()

        photos = Parser.driver.find_element(by=By.XPATH, value=xpath)
        img = photos.find_elements(by=By.TAG_NAME, value='img')
        images = []
        for i in img:
            image=Parser.parse_photo(i.get_attribute('src'))
            images.append(image)
            image.show()
        return images

p = Parser()
photo_storage_substring = {
    'nike': 'https://static.nike.com/a/images/'
}
# p.parse_photos(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700',
#               storage_substring=photo_storage_substring['nike'])
xpath_photos = {
    'nike': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[1]"""
}
p.parse_photos(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700', xpath=xpath_photos['nike'])