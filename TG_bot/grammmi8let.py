from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Замените на ваш токен
TOKEN = '7029933175:AAEI_Vx4kvq0IVEVruCyxt0uAzYkxaLtnj0'

# Список для хранения ID пользователей
user_ids = set()

# Функция для обработки новых сообщений
async def message_handler(update: Update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    # Добавляем ID пользователя в список, если его там нет
    if user_id not in user_ids:
        user_ids.add(user_id)
        print(f'Новый пользователь: {user_name} (ID: {user_id})')

# Функция для команды /start
async def start(update: Update, context):
    await update.message.reply_text('Бот работает! Отправьте сообщение, и я сохраню ваши ID.')

# Основная функция для запуска бота
def main():
    # Создаем объект Application
    application = Application.builder().token(TOKEN).build()
    
    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    
    # Обработчик всех сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
