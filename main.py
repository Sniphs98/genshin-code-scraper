from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import re

URL = "https://game8.co/games/Genshin-Impact/search?q=Redeem+Codes"
last_version_string = ""
version_string = "0.0"
new_version_bool = False
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
    global version_string
    pattern = "(\d+\.\d+)"
    newest_element = None
    for element in search_results:
        match = re.match(pattern, element.text, re.IGNORECASE)
        if match:
            if version_string < match.group(1):
                version_string = match.group(1)
                newest_element = element
                new_version_bool = True
    return newest_element

def write_newest_version_to_file():
    with open('last_version.txt', 'w') as file:
        file.write(highest_version_element.text)

def string_spliter(codes):
    code_dic = {}
    for code in codes:
        code_dic = code.split(')')
    return code_dic

search_results = driver.find_elements(By.CLASS_NAME, "c-archiveSearchListItem")
search_results = filter_redeem_codes(search_results)
highest_version_element = find_highest_version(search_results)

with open('last_version.txt', 'r') as file:
    last_version_string = file.read()

if(last_version_string):
    print("in last string")
    if(last_version_string.find(version_string)):
        print("-New Version")
        write_newest_version_to_file()
else:
        print("-Empty file")
        write_newest_version_to_file()
    

#temp = highest_version_element.find_element(By.XPATH, '//a[contains(@href, "440922")]')
element = highest_version_element.find_element(By.CLASS_NAME,"c-archiveSearchListItem__link")
element.click()
time.sleep(2)


tables = driver.find_elements(By.CLASS_NAME, "a-table")
#for table in tables:
    #print("-----------------------------------------------------------------")
    #print(table.get_attribute("innerHTML"))
codes = []
tr_elements = tables[0].find_elements(By.TAG_NAME,"tr")
for tr in tr_elements:
    center_elements = tr.find_elements(By.CLASS_NAME,"center")
    for element in center_elements:
        #print(element.text)
        codes.append(element.text)

title = "New Version is up "+ version_string +" 🚀🎉 "
return_string = ""
if new_version_bool:
    for code in codes:
        return_string = return_string + "- " + code + '\n'
    requests.post("https://ntfy.sh/genshin_codes",
            data=return_string.encode(encoding='utf-8'),
            headers={
                "Title": title.encode(encoding='utf-8'),
                "Tags" : "robot" ,
                "Click": "https://genshin.hoyoverse.com/de/gift",
                "Icon": "https://cdn3.emoji.gg/emojis/5579-primogem.png"
            })
print("finished.")



