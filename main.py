from playwright.sync_api import sync_playwright
import time
import re
from notification import NotificationService

# Configuration
GENSHIN_URL = "https://game8.co/games/Genshin-Impact/search?q=Livestream+Codes"
ZZZ_URL = "https://game8.co/games/Zenless-Zone-Zero/archives/435683"



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
    
    # Extract version number from stored string (remove game prefix)
    if last_version_string.startswith('genshin_'):
        stored_version = last_version_string.replace('genshin_', '')
    elif last_version_string.startswith('zzz_'):
        stored_version = last_version_string.replace('zzz_', '')
    else:
        stored_version = last_version_string
    
    # Compare versions numerically
    try:
        return float(current_version) > float(stored_version)
    except ValueError:
        # Fallback to string comparison if numeric conversion fails
        return stored_version != current_version

def scrape_genshin_codes(page):
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

def scrape_zzz_codes(page):
    codes = []
    
    # Look for table rows containing codes
    code_rows = page.locator("table tr").all()
    
    for row in code_rows:
        # Try to find code in the first cell
        cells = row.locator("td").all()
        if len(cells) >= 2:
            code_text = cells[0].text_content().strip()
            # Simple validation: codes are usually alphanumeric and 8+ characters
            if code_text and len(code_text) >= 8 and code_text.replace('_', '').replace('-', '').isalnum():
                codes.append(code_text)
    
    # Alternative: look for clipboard containers if they exist
    clipboard_elements = page.locator(".a-clipboard__container").all()
    for element in clipboard_elements:
        input_element = element.locator(".a-clipboard__textInput")
        if input_element.count() > 0:
            code_value = input_element.get_attribute("value")
            if code_value and code_value.strip():
                codes.append(code_value.strip())
    
    return codes

def format_genshin_notification_message(codes):
    message = "\n"
    for code in codes:
        redemption_link = f"https://genshin.hoyoverse.com/en/gift?code={code}"
        message += f"- {code}\n  {redemption_link}\n\n"
    return message

def format_zzz_notification_message(codes):
    message = "\n"
    for code in codes:
        redemption_link = f"https://zenless.hoyoverse.com/redemption?code={code}"
        message += f"- {code}\n  {redemption_link}\n\n"
    return message

def setup_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    return playwright, browser, page

def scrape_genshin():
    # Setup browser
    playwright, browser, page = setup_browser()
    
    try:
        # Navigate to page
        page.goto(GENSHIN_URL)
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
            # Convert to float for proper numeric comparison
            numeric_versions = [float(v) for v in versions]
            version_string = str(max(numeric_versions))
            print(f"Found Genshin version in text: {version_string}")
        else:
            version_string = "0.0"
            print("No Genshin version found in text")
        
        # Check if this is a new version
        last_version_string = read_last_version()
        new_version_bool = is_new_version(last_version_string, version_string)
        
        if new_version_bool:
            print("New Genshin version detected!")
            write_newest_version(f"genshin_{version_string}")
            
            time.sleep(1)
            
            # Scrape codes
            codes = scrape_genshin_codes(page)
            
            return codes, version_string, "genshin"
        else:
            print("No new Genshin version found.")
            return [], version_string, "genshin"
        
        
    finally:
        # Clean up
        browser.close()
        playwright.stop()

def scrape_zzz():
    # Setup browser  
    playwright, browser, page = setup_browser()
    
    try:
        # Navigate directly to ZZZ codes page
        page.goto(ZZZ_URL)
        page.wait_for_load_state('networkidle')
        
        # Handle cookie consent
        time.sleep(2)
        handle_cookie_consent(page)
        
        # Look for version info in page content
        page_content = page.content()
        pattern = r"(\d+\.\d+)"
        versions = re.findall(pattern, page_content)
        
        if versions:
            version_string = max(versions)
            print(f"Found ZZZ version: {version_string}")
        else:
            version_string = "1.0"
            print("No ZZZ version found, using default")
        
        # Check if this is a new version (use separate file for ZZZ)
        try:
            with open('last_zzz_version.txt', 'r') as file:
                last_zzz_version = file.read().strip()
        except FileNotFoundError:
            last_zzz_version = ""
        
        new_version_bool = is_new_version(last_zzz_version, version_string)
        
        if new_version_bool:
            print("New ZZZ version detected!")
            with open('last_zzz_version.txt', 'w') as file:
                file.write(f"zzz_{version_string}")
            
            # Scrape codes
            codes = scrape_zzz_codes(page)
            
            return codes, version_string, "zzz"
        else:
            print("No new ZZZ version found.")
            return [], version_string, "zzz"
        
    finally:
        # Clean up
        browser.close()
        playwright.stop()

def main():
    return_string = ""
    
    print("Checking Genshin Impact codes...")
    genshin_codes, genshin_version, _ = scrape_genshin()
    
    print("Checking Zenless Zone Zero codes...")
    zzz_codes, zzz_version, _ = scrape_zzz()
    
    # Send notifications if new codes found
    if genshin_codes:
        genshin_notifier = NotificationService(game_type="genshin")
        codes_for_notification = genshin_codes[:3]
        title = f"New Genshin Impact Version {genshin_version} 🚀🎉"
        notification_message = format_genshin_notification_message(codes_for_notification)
        return_string += f"GENSHIN IMPACT:\n{notification_message}\n"
        genshin_notifier.send_notification(title, notification_message)
    
    if zzz_codes:
        zzz_notifier = NotificationService(game_type="zzz")
        codes_for_notification = zzz_codes[:3]
        title = f"New Zenless Zone Zero Codes {zzz_version} ⚡🎉"
        notification_message = format_zzz_notification_message(codes_for_notification)
        return_string += f"ZENLESS ZONE ZERO:\n{notification_message}\n"
        zzz_notifier.send_notification(title, notification_message)
    
    if return_string:
        print(return_string)
    else:
        print("No new codes found for either game.")
    
    print("Finished")


if __name__ == "__main__":
    main()