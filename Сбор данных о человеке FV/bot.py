from datetime import datetime, timedelta

class Bot:
    def __init__(self, tg_api, json, prometheus):
        self.tg_api = tg_api
        self.json = json
        self.prometheus = prometheus

    def get_user_info(self, user_id):
        # Получение информации о пользователе
        return self.tg_api.get_user_info(user_id)

    def get_messages(self, chat_id, days=3):
        # Сбор сообщений за последние 'days' дней
        messages = []
        offset = 0
        while True:
            response = self.tg_api.get_messages(chat_id, offset)
            if 'result' in response:
                for msg in response['result']:
                    message = msg.get('message')
                    if message and message.get('date') and (datetime.now() - datetime.fromtimestamp(message['date'])) < timedelta(days=days):
                        messages.append({
                            'date': datetime.fromtimestamp(message['date']).strftime('%Y-%m-%d'),
                            'time': datetime.fromtimestamp(message['date']).strftime('%H:%M:%S'),
                            'text': message.get('text', '')  # Сохраняем только текст
                        })
                if len(response['result']) < 100:
                    break
                offset += 100
            else:
                break
        return messages

    def run(self, user_id, chat_id):
        # Главная функция
        user_info = self.get_user_info(user_id)
        messages = self.get_messages(chat_id)
        data = {
            'user_info': user_info,
            'messages': messages
        }
        self.json.save(data)  # Сохраняем в JSON
