import requests
import configparser

class NotificationService:
    def __init__(self, config_file="notification_config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Default values
        self.enabled = self.config.getboolean('notification', 'enabled', fallback=True)
        self.url = self.config.get('notification', 'url', fallback="https://ntfy.sh/genshin_codes")
        self.icon = self.config.get('notification', 'icon', fallback="https://cdn3.emoji.gg/emojis/5579-primogem.png")
        self.tags = self.config.get('notification', 'tags', fallback="robot")
    
    def send_notification(self, title, message):
        if not self.enabled:
            print("Notifications disabled")
            return
        
        try:
            response = requests.post(
                self.url,
                data=message.encode(encoding='utf-8'),
                headers={
                    "Title": title.encode(encoding='utf-8'),
                    "Tags": self.tags,
                    "Icon": self.icon,
                    "Actions": "view, Activate codes, https://ntfy.sh/genshin_codes"
                }
            )
            print(f"Notification sent: {response.status_code}")
        except Exception as e:
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