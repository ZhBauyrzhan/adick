from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


import time


PATH = 'C:\Program Files (x86)\chromedriver.exe'
opts = ChromeOptions()
opts.add_argument('— headless')
driver = Chrome(executable_path=PATH, options=opts)
driver.get('https://www.nike.com/t/free-metcon-5-mens-training-shoes-Vfsbpq/DV3949-700')
driver.maximize_window()
try:
    accept = driver.find_element(By.CLASS_NAME, 'nds-btn dialog-actions-accept-btn css-60b779 ex41m6f0 btn-primary-dark  btn-md')
    driver.find_element(By.XPATH, '//*[@id="modal-root"]/div/div/div/div/div/section/div[2]/div/button[1]').click()
    time.sleep(30)
    # // *[ @ id = "modal-root"] / div / div / div / div / div / section / div[2] / div / button[1]
    # divs = []
    # divs = driver.find_element(By.CLASS_NAME, 'd-sm-flx flx-jc-sm-fs flx-ai-sm-fe css-1mhv7vq')
    # print(divs)
    # for div in divs:
    #     image_source = div.find_element(By.XPATH, '.// *[ @ id = "PDP"]/div[2]/div/div[4]/div[2]/div[1]/div/div[1]/div[1]/label/img')
    #     print(image_source, 'was')
except:
    print('fail')
# class="d-sm-flx flx-jc-sm-fs flx-ai-sm-fe css-1mhv7vq"
# // *[ @ id = "PDP"] / div[2] / div / div[4] / div[2] / div[1] / div / div[1] / div[1] / label / img
# time.sleep(30000)