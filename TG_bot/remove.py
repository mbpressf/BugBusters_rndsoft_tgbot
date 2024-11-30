import json
from datetime import datetime
from telebot import TeleBot


# Файл для хранения данных
DATA_FILE = "deleted_users.json"

# Инициализация файла
def init_file():
    try:
        with open(DATA_FILE, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)

# Сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Загрузка данных из файла
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Логирование удаленного пользователя
def log_user_removal(user_id, chat_id, role):
    data = load_data()
    data.append({
        "user_id": user_id,
        "chat_id": chat_id,
        "role": role,
        "deleted_at": datetime.now().isoformat()
    })
    save_data(data)

# Восстановление пользователя
def restore_user(user_id):
    data = load_data()
    to_restore = [entry for entry in data if entry["user_id"] == user_id]

    if not to_restore:
        return f"Пользователь {user_id} не найден в списке удаленных."

    for entry in to_restore:
        chat_id = entry["chat_id"]
        role = entry["role"]
        try:
            bot.add_chat_member(chat_id, user_id)
            if role:
                bot.promote_chat_member(chat_id, user_id, **get_permissions(role))
        except Exception as e:
            print(f"Не удалось восстановить пользователя {user_id} в чате {chat_id}: {e}")

    # Удаляем записи после восстановления
    updated_data = [entry for entry in data if entry["user_id"] != user_id]
    save_data(updated_data)

    return f"Пользователь {user_id} успешно восстановлен."

# Преобразование роли в права
def get_permissions(role):
    if role == "admin":
        return {
            "can_change_info": True,
            "can_delete_messages": True,
            "can_invite_users": True,
            "can_pin_messages": True
        }
    return {}

# Обработчик команды удаления пользователя
@bot.message_handler(commands=['remove_user'])
def handle_remove(message):
    try:
        args = message.text.split()
        user_id = int(args[1])  # Например: /remove_user 12345
        chat_id = message.chat.id
        role = "admin"  # Пример роли, можно адаптировать под реальную логику

        # Удаление пользователя (эмуляция, бот должен быть админом)
        # bot.kick_chat_member(chat_id, user_id)

        # Логирование удаления
        log_user_removal(user_id, chat_id, role)
        bot.reply_to(message, f"Пользователь {user_id} удален и записан в лог.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Обработчик команды восстановления пользователя
@bot.message_handler(commands=['restore_user'])
def handle_restore(message):
    try:
        args = message.text.split()
        user_id = int(args[1])  # Например: /restore_user 12345
        result = restore_user(user_id)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Запуск бота
if name == "__main__":
    init_file()
    bot.polling()