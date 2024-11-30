from bot import Bot
from config import DATA_FILE, TELEGRAM_API_TOKEN
from services.tg_api import TgApi
from services.json import JSON
from services.prometheus import Prometheus
import os

def main():
    tg_api = TgApi(TELEGRAM_API_TOKEN)
    json = JSON(DATA_FILE)
    prometheus = Prometheus()
    bot = Bot(tg_api, json, prometheus)
    user_id = 848456806
    chat_id = -1002142184809
    bot.run(user_id, chat_id)

if __name__ == '__main__':
    main()