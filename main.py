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

game_name = 'Genshin Impact version'

def contains_numbers(text):
    for char in text:
        if char.isdigit():
            return True
    return False

def find_highest_version(search_results):
    version_string = "0"
    newest_element = None
    for element in search_results:
        if (game_name in element.text):
            ##print(element.text.split("version ")[1].split()[0])
            if float(element.text.split("version ")[1].split()[0]) > float(version_string):
                print(element.text.split("version ")[1].split()[0])
                version_string = element.text.split("version ")[1].split()[0]
                newest_element = element
    return newest_element

search_results = driver.find_elements(By.CLASS_NAME, "c-entry-box--compact__title")
with open('scraper.html', 'w') as file:
    element = find_highest_version(search_results)
    print(element.text)
    for element in search_results:
        file.write(element.get_attribute("innerHTML"))
        file.write("\n")

print("finished.")


