from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time

# serv = Service('C:/Program Files (x86)/chromedriver.exe')
# opts = ChromeOptions()
# # opts.headless = True
# driver = Chrome(service=serv, options=opts)
# driver.get('https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700')
# driver.maximize_window()
s = """M 3.5 / W 5
M 4 / W 5.5
M 4.5 / W 6
M 5 / W 6.5
M 5.5 / W 7
M 6 / W 7.5
M 6.5 / W 8
M 7 / W 8.5
M 7.5 / W 9
M 8 / W 9.5
M 8.5 / W 10
M 9 / W 10.5
M 9.5 / W 11
M 10 / W 11.5
M 10.5 / W 12
M 11 / W 12.5
M 11.5 / W 13
M 12 / W 13.5
M 12.5 / W 14
M 13 / W 14.5
M 14 / W 15.5
M 15 / W 16.5
M 3.5 / W 5"""


sizes = s.split('\n')
print(sizes)