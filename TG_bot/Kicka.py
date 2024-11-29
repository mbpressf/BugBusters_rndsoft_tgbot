import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота с токеном
bot_token = '7029933175:AAECVJR2O_cbPK1lCKdKh8UBD_DAydFsZIo'  # Замените на токен вашего бота
admin_id = '5405355475'  # Замените на ваш ID (это тот человек, который может отдавать команды)

# Функция для загрузки чатов из файла chats.json
def load_chats():
    try:
        with open('chats.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Возвращаем пустой словарь, если файл не существует или пуст

# Функция для сохранения чатов в файл
def save_chats(chats):
    logger.info(f"Сохраняем чаты: {chats}")  # Логирование перед сохранением
    with open('chats.json', 'w') as file:
        json.dump(chats, file)

# Функция для добавления чата в chats.json
async def add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что команда пришла от администратора
    if update.message.from_user.id != int(admin_id):
        await update.message.reply_text("У вас нет прав на выполнение этой команды.")
        return

    chat_id = update.effective_chat.id  # Получаем ID текущего чата

    # Загружаем текущие чаты из файла
    chats = load_chats()

    # Добавляем текущий чат в список чатов, если его ещё нет
    if chat_id not in chats:
        chats[chat_id] = {
            "chat_name": update.effective_chat.title,
            "chat_type": update.effective_chat.type
        }
        save_chats(chats)
        await update.message.reply_text(f"Чат с ID {chat_id} успешно добавлен в список чатов.")
    else:
        await update.message.reply_text(f"Чат с ID {chat_id} уже есть в списке.")

# Функция для сохранения ID пользователей
def save_user_ids(user_ids):
    logger.info(f"Сохраняем ID пользователей: {user_ids}")  # Логирование перед сохранением
    with open('user_ids.json', 'w') as file:
        json.dump(user_ids, file)

# Словарь для хранения ID пользователей по чатам
user_ids_dict = {}

# Функция для отслеживания добавления новых пользователей
async def track_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    new_user = update.message.new_chat_members[0]
    user_id = new_user.id  # Получаем ID нового участника

    # Логирование добавления нового пользователя
    logger.info(f"Добавлен новый пользователь: {user_id} в чат: {chat_id}")

    # Добавляем ID нового пользователя в список
    if chat_id not in user_ids_dict:
        user_ids_dict[chat_id] = []
    
    user_ids_dict[chat_id].append(user_id)

    # Логируем обновленный список
    logger.info(f"Обновленный список пользователей для чата {chat_id}: {user_ids_dict[chat_id]}")

    # Сохраняем обновленный список ID пользователей в файл
    save_user_ids(user_ids_dict)

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

# Функция для сбора всех ID пользователей из всех чатов
async def collect_user_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что команда пришла от администратора
    if update.message.from_user.id != int(admin_id):
        await update.message.reply_text("У вас нет прав на выполнение этой команды.")
        return

    # Загружаем чаты
    chats = load_chats()
    all_user_ids = []

    bot = Bot(token=bot_token)

    # Перебираем все чаты, чтобы собрать ID пользователей
    for chat_id in chats.keys():
        try:
            # Получаем администраторов чата
            administrators = await bot.get_chat_administrators(chat_id)
            for admin in administrators:
                all_user_ids.append(admin.user.id)  # Добавляем ID администратора
        except Exception as e:
            await update.message.reply_text(f"Не удалось получить администраторов чата {chat_id}: {e}")
            continue

    # Сохраняем все собранные ID пользователей в файл
    save_user_ids(all_user_ids)
    await update.message.reply_text(f"ID пользователей успешно собраны и сохранены.")




# Функция для получения всех участников чата (работает только для администраторов)
async def get_chat_members(update: Update, context):
    if update.message.from_user.id != admin_id:
        await update.message.reply_text("У вас нет прав на выполнение этой команды.")
        return

    chat_id = update.effective_chat.id

    try:
        bot = update.bot
        # Получаем количество участников
        members_count = await bot.get_chat_members_count(chat_id)
        all_users = []
        
        for i in range(members_count):
            member = await bot.get_chat_member(chat_id, i)
            all_users.append(member.user.id)
        
        # Сохраняем все ID участников
        save_user_ids(all_users)
        await update.message.reply_text(f"Собрано {len(all_users)} ID участников.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при получении участников чата: {e}")




# Основная функция для запуска бота
def main():
    application = Application.builder().token(bot_token).build()

    # Обработчик команды /kick для удаления пользователя
    application.add_handler(CommandHandler("kick", kick_user))

    # Обработчик команды /get_chat_members
    application.add_handler(CommandHandler("get_chat_members", get_chat_members))

    # Обработчик команды /collect_user_ids для сбора всех ID пользователей
    application.add_handler(CommandHandler("collect_user_ids", collect_user_ids))

    # Обработчик команды /add_chat для добавления чата в chats.json
    application.add_handler(CommandHandler("add_chat", add_chat))

    # Обработчик для отслеживания добавления новых пользователей
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_new_user))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
