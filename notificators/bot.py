import requests

token = os.environ.get('BOT_TOKEN')
client_id = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    token = token  # Your Bot Token
    chat_id = client_id  # Replace this with your chat ID
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'

    response = requests.get(send_text)
    return response.json()

# Example usage
message = "Hello, this is a test message from my Python script!"
result = send_telegram_message(message)
print(result)