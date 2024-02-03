from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

URL = "https://www.polygon.com/search?q=Genshin+Impact+version+"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL)
driver.implicitly_wait(5)
time.sleep(3)

elements = driver.find_elements(By.CLASS_NAME, "c-entry-box--compact__title")
with open('scraper.html', 'w') as file:
    for element in elements:
        file.write(element.get_attribute("innerHTML"))
        file.write("\n")

print("finished.")