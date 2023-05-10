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

        # print(fieldset.text)
        # time.sleep(1000)
        text: str = fieldset.text
        return text.split('\n')

    @staticmethod
    def _parse_photo(url: str) -> Image:
        with requests.get(url, headers=Parser.headers, stream=True).raw as raw_image:
            return Image.open(raw_image)

    # @staticmethod
    # def _parse_photos(driver: Chrome, xpath: str) -> list[Image]:
    #     photos = driver.find_element(by=By.XPATH, value=xpath)
    #     img = photos.find_elements(by=By.TAG_NAME, value='img')
    #     images = []
    #     for i in img:
    #         image = Parser._parse_photo(i.get_attribute('src'))
    #         images.append(image)
    #         # image.show()
    #     return images

    @staticmethod
    def _parse_photos(driver: Chrome, xpath: str) -> list[Image]:

        container = driver.find_element(by=By.XPATH, value=xpath)
        photos = container.find_elements(by=By.TAG_NAME, value='img')
        # photos = driver.find_elements(by=By.TAG_NAME, value='img')

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
        print(name)
        return name

    @staticmethod
    def _parse_price(driver: Chrome, xpath: str) -> str:
        price = driver.find_element(by=By.XPATH, value=xpath).text
        print(price)
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
    def parse_items(url: str, xpath: dict) -> None:
        opts = ChromeOptions()
        # opts.headless = True
        driver = Chrome(service=Parser.serv, options=opts)
        driver.get(url)
        driver.maximize_window()
        # time.sleep(3000)
        Parser._country(driver=driver, xpath=xpath['country'])
        Parser._cookies(driver=driver, xpath=xpath['accept'])
        time.sleep(25)
        name = Parser._parse_name(driver=driver, xpath=xpath['name'])
        price = Parser._parse_price(driver=driver, xpath=xpath['price'])
        # images = Parser._parse_photos(driver=driver, xpath=xpath['photos'])
        # try:
        #     for i in images:
        #         i.show()
        # except Exception as e:
        #     print(e)
        sizes = Parser._parse_size(driver=driver, xpath=xpath['size'])
        print(sizes)
        driver.close()

    @staticmethod
    def parse_item_grid(url: str, xpath: dict) -> None:
        opts = ChromeOptions()
        # opts.headless = True
        driver = Chrome(service=Parser.serv, options=opts)
        driver.get(url)
        driver.maximize_window()
        Parser._country(driver=driver, xpath=xpath['country'])
        Parser._cookies(driver=driver, xpath=xpath['accept'])
        time.sleep(25)
        divs = driver.find_elements(by=By.CLASS_NAME, value='product-card')
        for i in divs:
            link = i.find_element(by=By.TAG_NAME, value='a')
            print(link.get_attribute('href'))
        # grid = driver.find_element(by=By.XPATH, value=xpath_nike['grid'])
        # links = grid.find_elements(by=By.TAG_NAME, value='a')
        # for i in links:
        #     print(i.get_attribute('href'))


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
    'photos': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[2]""",
    'size': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div""",
    'accept': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]""",
    'decline': """/html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[2]""",
    'name': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h1""",
    'price': """/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div
    /div[2]/div/div/div/div/div""",
    'country': """/html/body/div[6]/div/div/nav/button""",
    'grid':  """/html/body/div[4]/div/div/div[2]/div[4]/div/div[5]/div[2]"""
}

# p.parse_shoes(url='https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700', xpath=xpath_nike)

# p.parse_items(url='https://www.nike.com/t/air-zoom-flight-95-mens-shoes-zc42bP/DX5505-100', xpath=xpath_nike)

p.parse_item_grid(url='https://www.nike.com/w/mens-shoes-nik1zy7ok', xpath=xpath_nike)

# photo 1 /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[2]

# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div
# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div/div[1]
# /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[3]/form/div[1]/fieldset/div/div[17]

# name /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h1

# price /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div

# star /html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[4]/div/details[2]/summary/div
# aria-label="4.8"

# accept /html/body/div[7]/div/div/div/div/div/section/div[2]/div/button[1]
# decline /html/body/div[7]/div/div/div/div/div/section/div[2]/div/butt on[2]
