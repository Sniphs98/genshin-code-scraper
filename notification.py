# notification.py
import requests
import configparser

class NotificationService:
    def __init__(self, config_file="notification_config.ini", game_type="genshin"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.game_type = game_type
        
        if game_type == "zzz":
            self.redemption_url_base = "https://zenless.hoyoverse.com/redemption?code="
        else:
            self.redemption_url_base = "https://genshin.hoyoverse.com/en/gift?code="
        
        default_url = f"https://ntfy.sh/{game_type}_codes"
        default_icon = "https://cdn3.emoji.gg/emojis/5579-primogem.png" if game_type == "genshin" else "https://static.wikia.nocookie.net/zenless-zone-zero/images/8/8b/Ether_Battery.png"

        self.enabled = self.config.getboolean('notification', 'enabled', fallback=True)
        self.url = self.config.get('notification', f'{game_type}_url', fallback=default_url)
        self.icon = self.config.get('notification', f'{game_type}_icon', fallback=default_icon)
        self.tags = self.config.get('notification', 'tags', fallback="robot")
    
    def send_notification(self, title, codes):
        if not self.enabled:
            print("Notifications disabled")
            return

        try:
            markdown_links = []
            for code in codes:
                link_url = f"{self.redemption_url_base}{code}"
                link_text = f"[{code}]({link_url})"
                markdown_links.append(link_text)
            
            message = "\n".join(markdown_links)

            # Action button to open web version where links are clickable
            actions_header = f"view, Open Web Version, {self.url}"
            
            headers = {
                "Title": title,
                "Tags": self.tags,
                "Icon": self.icon,
                "Actions": actions_header
            }
            
            response = requests.post(
                self.url,
                data=message.encode(encoding='utf-8'),
                headers=headers
            )
            response.raise_for_status()
            print(f"Notification sent successfully: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send notification: {e}")

def create_default_config():
    config = configparser.ConfigParser()
    config['notification'] = {
        'enabled': 'true',
        'url': 'https://ntfy.sh/genshin_codes',
        'icon': 'https://cdn3.emoji.gg/emojis/5579-primogem.png',
        'tags': 'robot'
    }
    
    with open('notification_config.ini', 'w') as configfile:
        config.write(configfile)
    print("Created default notification_config.ini")

if __name__ == "__main__":
    create_default_config()