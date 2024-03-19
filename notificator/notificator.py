import requests
import os

token = os.environ.get('BOT_TOKEN')
client_id = os.environ.get('CHAT_ID')

class Notificator:
    def __init__(self):
        pass
    def configure_telegram(self, use_env_variables=True):
        self.telegram_bot_token= os.environ.get('BOT_TOKEN')
        self.telegram_CHAT_ID = os.environ.get('CHAT_ID')

    def send_telegram_message(self,message):

        send_text = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage?chat_id={ self.telegram_CHAT_ID}&text={message}'

        response = requests.get(send_text)
        return response.json()

# Example usage

notif=Notificator()
notif.configure_telegram()
message = "Hello, this is a test message from my Python script!"

result = notif.send_telegram_message(message)
print(result)