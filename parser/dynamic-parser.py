from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time

serv = Service('C:/Program Files (x86)/chromedriver.exe')
opts = ChromeOptions()
# opts.headless = True
driver = Chrome(service=serv, options=opts)
driver.get('https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700')
driver.maximize_window()
try:
    photos = driver.find_element(by=By.XPATH, value="""/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[1]""")
    photos_containers = driver.find_element(by=By.XPATH, value="""/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div""")
    big = driver.find_element(by=By.XPATH, value="""/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[1]/div/div[2]/div[1]""")

    images = driver.find_elements(by=By.PARTIAL_LINK_TEXT, value="""https://static.nike.com/a/images/""")

    for i in images:
        print(i.get_attribute('src'))

    print(photos.text, '1')
    print('********************************************************')
    print(photos_containers.text, '2')
    img = photos.find_elements(by=By.TAG_NAME, value='img')
    image_sources = []
    for i in img:
        image_sources.append( i.get_attribute('src') )
    print(image_sources)


    time.sleep(3000)
except Exception as e:
    print('fail', e)