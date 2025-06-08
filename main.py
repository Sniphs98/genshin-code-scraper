from playwright.sync_api import sync_playwright
import time
import re
from notification import NotificationService

# Configuration
URL = "https://game8.co/games/Genshin-Impact/search?q=Livestream+Codes"



def handle_cookie_consent(page):
    try:
        cookies_button = page.get_by_text("Do not consent")
        cookies_button.click()
    except Exception:
        print("No cookie 1 banner!")
   
def goToCodePage(page):
    try:
        # First try to find specific link with version and codes
        code_button = page.get_by_text("5.7 Livestream Codes List").first()
        code_button.click()
    except Exception:
        try:
            # Fallback: look for any livestream codes link
            code_button = page.locator("a:has-text('Livestream Codes')").first()
            code_button.click()
        except Exception:
            # Last resort: direct navigation
            page.goto("https://game8.co/games/Genshin-Impact/archives/304759")
            print("Used direct navigation to codes page")
        
def get_code_from_string(code_string):
    parts = code_string.strip().split()
    if parts:
        return parts[0]
    return None

def get_codes_from_string(codes_string):
    codes = []
    lines = codes_string.splitlines()
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            code = get_code_from_string(line)
            if code:  # Only add non-empty codes
                codes.append(code)
    return codes

def find_highest_version(search_results):
    pattern = r"(\d+\.\d+)"
    newest_element = None
    highest_version = "0.0"
    
    for element in search_results:
        match = re.match(pattern, element.text_content(), re.IGNORECASE)
        if match:
            if highest_version < match.group(1):
                highest_version = match.group(1)
                newest_element = element
    
    return newest_element, highest_version

def read_last_version():
    try:
        with open('last_version.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def write_newest_version(version_text):
    with open('last_version.txt', 'w') as file:
        file.write(version_text)

def is_new_version(last_version_string, current_version):
    if not last_version_string:
        return True
    return last_version_string.find(current_version) == -1

def scrape_codes(page):
    clipboard_elements = page.locator(".a-clipboard__container").all()
    if not clipboard_elements:
        return []
    
    codes = []
    for element in clipboard_elements:
        input_element = element.locator(".a-clipboard__textInput")
        if input_element.count() > 0:
            code_value = input_element.get_attribute("value")
            if code_value and code_value.strip():
                codes.append(code_value.strip())
    
    return codes

def format_notification_message(codes):
    message = "\n"
    for code in codes:
        redemption_link = f"https://genshin.hoyoverse.com/en/gift?code={code}"
        message += f"- {code}\n  {redemption_link}\n\n"
    return message

def setup_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    return playwright, browser, page

def main():
    return_string = ""
    
    # Setup notification service
    notifier = NotificationService()
    
    # Setup browser
    playwright, browser, page = setup_browser()
    
    try:
        # Navigate to page
        page.goto(URL)
        page.wait_for_load_state('networkidle')
        
        
        # Handle cookie consent
        time.sleep(2)
        handle_cookie_consent(page)
        
        goToCodePage(page)

        # Find highest version from main div text
        main_div = page.locator("body > div.p-archiveBody__container > div.p-archiveBody__main > div.p-archiveContent__container > div.p-archiveContent__main")
        div_text = main_div.text_content()
        
        # Search for versions in text
        pattern = r"(\d+\.\d+)"
        versions = re.findall(pattern, div_text)
        
        if versions:
            version_string = max(versions)
            print(f"Found version in text: {version_string}")
        else:
            version_string = "0.0"
            print("No version found in text")
        
        # Check if this is a new version
        last_version_string = read_last_version()
        new_version_bool = is_new_version(last_version_string, version_string)
        
        if new_version_bool:
            print("New version detected!")
            write_newest_version(version_string)
            
            # Navigate to codes page (simplified - you may need to adjust this)
            # Since we found version in text, we need to find the actual link
            time.sleep(1)
            
            # Scrape codes
            codes = scrape_codes(page)
            
            # Only take first 3 codes for notification
            codes_for_notification = codes[:3]
            
            # Send notification
            title = f"New Version is up {version_string} 🚀🎉"
            notification_message = format_notification_message(codes_for_notification)
            return_string += notification_message
            
            print(return_string)
            notifier.send_notification(title, return_string)
        else:
            print("No new version found.")
        
        print("Finished")
        
    finally:
        # Clean up
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    main()