from flask import Flask, jsonify, request
from flask_cors import CORS
import telebot
from threading import Thread
import json

# Инициализация Flask
app = Flask(__name__)
CORS(app)

# Инициализация Telebot
BOT_TOKEN = "8054989054:AAERvIHaSiZ4IVFqnYE92Eva7GEFo0YJ2c4"
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для загрузки данных из файла
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 1. API для Vue.js
@app.route('/api/data', methods=['GET'])
def get_data():
    """Возвращает данные из файла data.json."""
    data = load_data()
    return jsonify(data)

# 2. Команда бота для проверки
@bot.message_handler(commands=['start'])
def handle_start(message):
    data = load_data()
    bot.reply_to(message, f"Данные успешно загружены: {data['user_info']['first_name']}")

# 3. Запуск Flask и Telebot параллельно
def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_telebot():
    bot.polling()

if __name__ == '__main__':
    Thread(target=run_flask).start()
    Thread(target=run_telebot).start()
