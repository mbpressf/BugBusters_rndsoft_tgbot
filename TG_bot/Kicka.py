import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота с токеном
bot_token = '7029933175:AAECVJR2O_cbPK1lCKdKh8UBD_DAydFsZIo'  # Замените на токен вашего бота
admin_id = '5405355475'  # Замените на ваш ID (это тот человек, который может отдавать команды)

# Загружаем чаты из файла chats.json
def load_chats():
    with open('chats.json', 'r') as file:
        return json.load(file)

# Функция для удаления пользователя
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что команда пришла от администратора
    if update.message.from_user.id != int(admin_id):
        await update.message.reply_text("У вас нет прав на выполнение этой команды.")
        return

    # Получаем ID пользователя и ID чатов из аргументов команды
    try:
        user_id = int(context.args[0])  # ID пользователя, которого нужно удалить
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста, укажите ID пользователя для удаления.")
        return

    # Загружаем чаты
    chats = load_chats()

    # Перебираем все чаты, чтобы удалить пользователя
    for chat_id in chats.keys():
        try:
            bot = Bot(token=bot_token)
            await bot.ban_chat_member(chat_id, user_id)  # Используем ban_chat_member
            await update.message.reply_text(f"Пользователь {user_id} был удален из чата {chat_id}")
        except Exception as e:
            await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")

# Основная функция для запуска бота
def main():
    application = Application.builder().token(bot_token).build()

    # Обработчик команды /kick для удаления пользователя
    application.add_handler(CommandHandler("kick", kick_user))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()