import requests

class TgApi:
    def __init__(self, token):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{token}'

    def get_user_info(self, user_id):
        # Получение данных профиля пользователя
        url = f'{self.base_url}/getChat?chat_id={user_id}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('result', {})
        return {}

    def get_messages(self, chat_id, offset):
        # Получение сообщений из чата
        url = f'{self.base_url}/getUpdates?chat_id={chat_id}&offset={offset}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {}
