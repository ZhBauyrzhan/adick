from PIL import Image
import requests

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class Parser:
    serv = Service('C:/Program Files (x86)/chromedriver.exe')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

    @staticmethod
    def _parse_size(driver: Chrome, xpath: str) -> list[str]:
        # time.sleep(10)
        # time.sleep(5)
        fieldset = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        print(fieldset.text)
        # time.sleep(1000)
        # return []
        div_container = fieldset.find_element(by=By.TAG_NAME, value='div')
        # divs = driver.find_elements(by=By.TAG_NAME, value='div')
        print(div_container.text)
        return []
        divs = div_container.find_elements(by=By.TAG_NAME, value='div')
        sizes: list[str] = []
        for div in divs:
            size = div.find_element(by=By.TAG_NAME, value='label').text
            disabled = div.find_element(by=By.TAG_NAME, value='input').get_attribute('disabled')
            if disabled is None:
                sizes.append(size)
        return sizes

    @staticmethod
    def _parse_photo(url: str) -> Image:
        with requests.get(url, headers=Parser.headers, stream=True).raw as raw_image:
            return Image.open(raw_image)

    @staticmethod
    def _parse_photos(driver: Chrome, xpath: str) -> list[Image]:
        photos = driver.find_element(by=By.XPATH, value=xpath)
        img = photos.find_elements(by=By.TAG_NAME, value='img')
        images = []
        for i in img:
            image = Parser._parse_photo(i.get_attribute('src'))
            images.append(image)
            # image.show()
        return images

    @staticmethod
    def _cookies(driver: Chrome, xpath: str) -> None:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        time.sleep(2)
        button.click()

    @staticmethod
    def _parse_name(driver: Chrome, xpath: str) -> str:
        name = driver.find_element(by=By.XPATH, value=xpath).text
        print(name)
        return name

    @staticmethod
    def _parse_price(driver: Chrome, xpath: str) -> str:
        price = driver.find_element(by=By.XPATH, value=xpath).text
        print(price)
        return price

    @staticmethod
    def parse_shoes(url: str, xpath: dict) -> None:
        opts = ChromeOptions()
        # opts.headless = True
        driver = Chrome(service=Parser.serv, options=opts)
        driver.get(url)
        driver.maximize_window()
        # time.sleep(3000)
        Parser._cookies(driver=driver, xpath=xpath['accept'])
        time.sleep(25)
        sizes = Parser._parse_size(driver=driver, xpath=xpath['size'])
        name = Parser._parse_name(driver=driver, xpath=xpath['name'])
        price = Parser._parse_price(driver=driver, xpath=xpath['price'])
        images = Parser._parse_photos(driver=driver, xpath=xpath['photos'])
        try:
            for i in images:
                i.show()
        except Exception as e:
            print(e)
p = Parser()
# xpath_photos = {
#     'nike': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[1]"""
# }
# p.parse_photos(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700', xpath=xpath_photos['nike'])
# xpath_size = {
#     'nike': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset"""
# }
# xpath_cookies = {
#     'nike-accept': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]""",
#     'nike-decline': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[2]""",
# }

xpath_nike = {
    'photos': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[1]""",
    'size': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset""",
    'accept': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]""",
    'decline': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[2]""",
    'name': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h1""",
    'price': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div
    /div[2]/div/div/div/div/div""",
}

p.parse_shoes(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700', xpath=xpath_nike)

# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div
# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div/div[1]
# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div/div[17]

# name /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h1

# price /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div

# star /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[4]/div/details[2]/summary/div
# aria-label="4.8"

# accept /html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]
# decline /html/body/div[7]/div/div/div/div/div/section/div[2]/div/butt on[2]
