from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re

URL = "https://game8.co/games/Genshin-Impact/search?q=Redeem+Codes"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL)
driver.implicitly_wait(5)
time.sleep(2)

search_string = 'Redeem Codes'

def contains_numbers(text):
    for char in text:
        if char.isdigit():
            return True
    return False

def filter_redeem_codes(search_results):
    redeem_codes_list = []
    for element in search_results:
        if (search_string in element.text):
            redeem_codes_list.append(element)
    return redeem_codes_list

def find_highest_version(search_results):
    pattern = "(\d+\.\d+)"
    newest_element = None
    version_string = "0.0"
    for element in search_results:
        match = re.match(pattern, element.text, re.IGNORECASE)
        if match:
            if version_string < match.group(1):
                version_string = match.group(1)
                newest_element = element
    return newest_element

search_results = driver.find_elements(By.CLASS_NAME, "c-archiveSearchListItem")
search_results = filter_redeem_codes(search_results)
highest_version_element = find_highest_version(search_results)

#search_results[1].get_attribute("innerHTML")
print(highest_version_element.get_attribute("href"))





#with open('scraper.html', 'w') as file:
#    for element in search_results:
#        file.write(element.get_attribute("innerHTML"))
#        file.write("\n")


print("finished.")


