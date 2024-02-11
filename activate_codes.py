from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://genshin.hoyoverse.com/de/gift")
driver.implicitly_wait(10)

element = driver.find_element(By.CLASS_NAME,"cdkey-select__menu")
print(element.get_attribute("innerHTML"))
print("-----------")
elements = element.find_elements(By.CLASS_NAME,"cdkey-select__option")
for e in elements:
    if e.get_attribute("innerHTML").find("Europe"):
        e.click()
time.sleep(5)