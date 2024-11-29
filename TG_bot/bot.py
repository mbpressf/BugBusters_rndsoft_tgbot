import telebot
import json
import os

# Замените на ваш токен бота
API_TOKEN = '7029933175:AAECVJR2O_cbPK1lCKdKh8UBD_DAydFsZIo'

bot = telebot.TeleBot(API_TOKEN)

# Пути к файлам JSON
admins_file = 'admins.json'
chats_file = 'chats.json'

# Загрузка данных из файлов JSON
def load_data():
    if os.path.exists(admins_file):
        with open(admins_file, 'r') as f:
            admins = json.load(f)
    else:
        admins = {}

    if os.path.exists(chats_file):
        with open(chats_file, 'r') as f:
            chat_list = json.load(f)
    else:
        chat_list = {}

    return admins, chat_list

# Сохранение данных в файлы JSON
def save_data():
    with open(admins_file, 'w') as f:
        json.dump(admins, f, ensure_ascii=False, indent=4)
    with open(chats_file, 'w') as f:
        json.dump(chat_list, f, ensure_ascii=False, indent=4)

# Загрузка начальных данных
admins, chat_list = load_data()

# Функция для добавления чатов
def add_chat(chat_id):
    if chat_id not in chat_list:
        chat_list[chat_id] = []
        save_data()  # Сохраняем данные

# Функция для добавления администратора
def set_admin(user_id):
    if user_id not in admins:
        admins[user_id] = True
        save_data()  # Сохраняем данные

# Команда /start для установки администратора
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    set_admin(user_id)
    bot.send_message(message.chat.id, "Бот настроен. Вы стали администратором.")

# Команда /add_chat для добавления текущего чата
@bot.message_handler(commands=['add_chat'])
def add_chat_command(message):
    user_id = message.from_user.id

    # Проверка, является ли отправитель администратором
    if user_id not in admins:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return

    # Получаем ID чата и добавляем его в список
    chat_id = message.chat.id
    add_chat(chat_id)
    bot.send_message(message.chat.id, f"Чат {chat_id} был добавлен в список чатов.")

# Команда /delete для удаления пользователя из всех чатов
@bot.message_handler(commands=['delete'])
def delete_user(message):
    user_id = message.from_user.id

    # Проверка, является ли отправитель администратором
    if user_id not in admins:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return

    # Извлекаем никнейм пользователя для удаления
    if message.text.startswith('/delete @'):
        username = message.text[len('/delete @'):].strip()

        if not username:
            bot.send_message(message.chat.id, "Пожалуйста, укажите пользователя для удаления.")
            return
        
        # Перебираем чаты, из которых нужно удалить пользователя
        deleted_count = 0
        for chat_id in chat_list.keys():
            try:
                # Проверка, является ли данный пользователь частью чата
                chat_members = bot.get_chat_administrators(chat_id)
                for member in chat_members:
                    if member.user.username == username:
                        bot.kick_chat_member(chat_id, member.user.id)
                        deleted_count += 1
                        break
            except Exception as e:
                # Пропуск чатов с ошибками, такими как "невозможно удалить владельца"
                if "Bad Request: can't remove chat owner" in str(e):
                    print(f"Пропущен чат {chat_id} (не удается удалить владельца).")
                else:
                    print(f"Ошибка при удалении пользователя из чата {chat_id}: {e}")

        if deleted_count > 0:
            bot.send_message(message.chat.id, f"Пользователь @{username} был удален из {deleted_count} чатов.")
        else:
            bot.send_message(message.chat.id, f"Пользователь @{username} не найден в чате или не может быть удален.")

    else:
        bot.send_message(message.chat.id, "Неверная команда. Используйте: /delete @<никнейм>")

# Запуск бота
bot.polling(none_stop=True)
