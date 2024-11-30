from prometheus_client import Counter

class Prometheus:
    def __init__(self):
        self.counter = Counter('tg_bot_messages', 'Количество сообщений в Telegram')

    def increment(self, value):
        self.counter.inc(value)