import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
from telegram.ext import ChatMemberHandler


# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



# Инициализация бота с токеном
bot_token = '7029933175:AAEI_Vx4kvq0IVEVruCyxt0uAzYkxaLtnj0'  # Замените на токен вашего бота
admin_id = '7004441787','5405355475'  # Замените на ваш ID (это тот человек, который может отдавать команды)



# Функция для загрузки чатов из файла chats.json с указанием кодировки
def load_chats():
    try:
        with open('chats.json', 'r', encoding='utf-8') as file:  
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  
    except UnicodeDecodeError as e:
        logger.error(f"Ошибка декодирования файла: {e}")
        return {}  

# Функция для сохранения чатов в файл
def save_chats(chats):
    logger.info(f"Сохраняем чаты: {chats}")  
    with open('chats.json', 'w', encoding='utf-8') as file:
        json.dump(chats, file, ensure_ascii=False, indent=4)

# Функция для сохранения ID пользователей
def save_user_ids(user_ids):
    user_ids_dict_serializable = {str(chat_id): list(user_ids_set) for chat_id, user_ids_set in user_ids.items()}
    
    logger.info(f"Сохраняем ID пользователей: {user_ids_dict_serializable}") 
    with open('user_ids.json', 'w', encoding='utf-8') as file:
        json.dump(user_ids_dict_serializable, file, ensure_ascii=False, indent=4)

def load_user_ids():
    try:
        with open('user_ids.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Преобразуем списки обратно в множества
            return {int(chat_id): set(user_ids) for chat_id, user_ids in data.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Словарь для хранения ID пользователей по чатам
user_ids_dict = load_user_ids()


# Функция для отслеживания добавления новых пользователей
async def track_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    new_user = update.message.new_chat_members[0]
    user_id = new_user.id  # Получаем ID нового участника

    # Логирование добавления нового пользователя
    logger.info(f"Добавлен новый пользователь: {user_id} в чат: {chat_id}")

    # Загружаем текущий список пользователей
    if chat_id not in user_ids_dict:
        user_ids_dict[chat_id] = set()  # Используем set для уникальности пользователей
    
    # Добавляем ID пользователя в set
    user_ids_dict[chat_id].add(user_id)

    # Логируем обновленный список
    logger.info(f"Обновленный список пользователей для чата {chat_id}: {user_ids_dict[chat_id]}")

    # Сохраняем обновленный список ID пользователей в файл
    save_user_ids(user_ids_dict)



# # Функция для удаления пользователя
# async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Проверка, что команда пришла от администратора
#     if update.message.from_user.id != int(admin_id):
#         await update.message.reply_text("У вас нет прав на выполнение этой команды.")
#         return

#     # Получаем ID пользователя и ID чатов из аргументов команды
#     try:
#         user_id = int(context.args[0])  # ID пользователя, которого нужно удалить
#     except (IndexError, ValueError):
#         await update.message.reply_text("Пожалуйста, укажите ID пользователя для удаления.")
#         return

#     # Загружаем чаты
#     chats = load_chats()

#     # Перебираем все чаты, чтобы удалить пользователя
#     for chat_id in chats.keys():
#         try:
#             bot = Bot(token=bot_token)
#             await bot.ban_chat_member(chat_id, user_id)  # Используем ban_chat_member
#             await update.message.reply_text(f"Пользователь {user_id} был удален из чата {chat_id}")
#         except Exception as e:
#             await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")

# async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Проверка, что команда пришла от администратора
#     if update.message.from_user.id != int(admin_id):
#         await update.message.reply_text("У вас нет прав на выполнение этой команды.")
#         return

#     # Получаем ID пользователя и ID чатов из аргументов команды
#     try:
#         user_id = int(context.args[0])  # ID пользователя, которого нужно удалить
#     except (IndexError, ValueError):
#         await update.message.reply_text("Пожалуйста, укажите ID пользователя для удаления.")
#         return

#     # Загружаем чаты
#     chats = load_chats()

#     # Перебираем все чаты, чтобы проверить, является ли отправитель администратором
#     for chat_id, chat_info in chats.items():
#         try:
#             bot = Bot(token=bot_token)
#             administrators = await bot.get_chat_administrators(chat_id)

#             # Проверяем, является ли отправитель команды администратором в этом чате
#             if update.message.from_user.id not in [admin.user.id for admin in administrators]:
#                 await update.message.reply_text(f"Вы не являетесь администратором в чате {chat_id}.")
#                 continue  # Пропускаем этот чат, если отправитель не администратор

#             # Если отправитель является администратором, удаляем пользователя
#             await bot.ban_chat_member(chat_id, user_id)  # Используем ban_chat_member
#             chat_name = chat_info.get('chat_name')
#             await update.message.reply_text(f"Пользователь c {user_id} был удален из чата {chat_id},{chat_name}")

#         except Exception as e:
#             await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")

import re

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы MarkdownV2."""
    text = re.sub(r'([\\`*_{}[\]()#+\-.!_])', r'\\\1', text)  # Экранируем обычные специальные символы
    text = text.replace('(', r'\(').replace(')', r'\)')  # Экранируем круглые скобки
    return text




# async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Проверка, что команда пришла от администратора
#     if update.message.from_user.id != int(admin_id):
#         await update.message.reply_text("У вас нет прав на выполнение этой команды.")
#         return

#     # Получаем ID пользователя и ID чатов из аргументов команды
#     try:
#         user_id = int(context.args[0])  # ID пользователя, которого нужно удалить
#     except (IndexError, ValueError):
#         await update.message.reply_text("Пожалуйста, укажите ID пользователя для удаления.")
#         return

#     # Загружаем чаты
#     chats = load_chats()

#     # Перебираем все чаты, чтобы проверить, является ли отправитель администратором
#     for chat_id, chat_info in chats.items():
#         try:
#             bot = Bot(token=bot_token)
#             administrators = await bot.get_chat_administrators(chat_id)

#             # Проверяем, является ли отправитель команды администратором в этом чате
#             if update.message.from_user.id not in [admin.user.id for admin in administrators]:
#                 await update.message.reply_text(f"Вы не являетесь администратором в чате {chat_id}.")
#                 continue  # Пропускаем этот чат, если отправитель не администратор

#             # Получаем имя пользователя
#             user = await bot.get_chat_member(chat_id, user_id)
#             user_name = user.user.username if user.user.username else f"{user.user.first_name} {user.user.last_name}"

#             # Получаем имя чата
#             chat_name = chat_info.get('chat_name', 'Неизвестный чат')

#             # Экранируем специальные символы в именах пользователя и чата
#             user_name = escape_markdown_v2(user_name)
#             chat_name = escape_markdown_v2(chat_name)

#             # Если отправитель является администратором, удаляем пользователя
#             await bot.ban_chat_member(chat_id, user_id)  # Используем ban_chat_member

#             # Формируем сообщение с использованием MarkdownV2 и скрытия текста
#             message = (
#                 f"Пользователь: @{user_name} \(ID: ||\{user_id}||\)\n"
#                 f"был удален с чата: {chat_name} \(ID: ||\{chat_id}||\)"
#             )

#             # Отправляем сообщение в формате MarkdownV2
#             await update.message.reply_text(message, parse_mode='MarkdownV2')

#         except Exception as e:
#             await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")


import time
from httpx import ConnectError

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

    # Перебираем все чаты, чтобы проверить, является ли отправитель администратором
    for chat_id, chat_info in chats.items():
        attempts = 3  # Количество попыток
        for attempt in range(attempts):
            try:
                bot = Bot(token=bot_token)
                administrators = await bot.get_chat_administrators(chat_id)

                # Проверяем, является ли отправитель команды администратором в этом чате
                if update.message.from_user.id not in [admin.user.id for admin in administrators]:
                    await update.message.reply_text(f"Вы не являетесь администратором в чате {chat_id}.")
                    continue  # Пропускаем этот чат, если отправитель не администратор

                # Получаем информацию о пользователе
                user = await bot.get_chat_member(chat_id, user_id)
                user_name = user.user.username if user.user.username else f"{user.user.first_name} {user.user.last_name}"
                user_status = user.status  # Статус пользователя в чате

                # Если пользователь не забанен, пытаемся получить дату присоединения
                user_joined = 'Неизвестно'
                if user_status != 'banned' and hasattr(user, 'joined_date') and user.joined_date:
                    user_joined = user.joined_date.strftime('%Y-%m-%d %H:%M:%S')

                # Получаем имя чата и другую информацию
                chat_name = chat_info.get('chat_name', 'Неизвестный чат')
                chat_title = await bot.get_chat(chat_id)  # Для получения дополнительных данных о чате
                chat_type = chat_title.type  # Тип чата: канал, группа, супергруппа и т.д.
                chat_description = chat_title.description if chat_title.description else 'Нет описания'

                # Экранируем специальные символы в именах пользователя и чата
                user_name = escape_markdown_v2(user_name)
                chat_name = escape_markdown_v2(chat_name)

                # Если отправитель является администратором, удаляем пользователя
                await bot.ban_chat_member(chat_id, user_id)  # Используем ban_chat_member

                # Формируем сообщение с использованием MarkdownV2 и скрытия текста
                message = (
                    f"Пользователь: @{user_name} \(ID: ||\{user_id}||\)\n"
                    f"Статус в чате: {user_status}\n"
                    f"Дата присоединения: {user_joined}\n\n"
                    f"Чат: {chat_name} \(ID: ||\{chat_id}||\)\n"
                    f"Тип чата: {chat_type}\n"
                    f"Описание чата: {chat_description}\n\n"
                    f"Пользователь был удален из чата."
                )

                # Отправляем сообщение в формате MarkdownV2
                await update.message.reply_text(message, parse_mode='MarkdownV2')

                break  # Прерываем цикл повторных попыток, если операция выполнена успешно

            except ConnectError as e:
                if attempt < attempts - 1:
                    await update.message.reply_text(f"Ошибка подключения, повторная попытка через 3 секунды... ({attempt + 1}/{attempts})")
                    time.sleep(3)  # Задержка между попытками
                else:
                    await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")





# Функция для сбора всех ID пользователей из всех чатов
async def collect_user_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что команда пришла от администратора
    if update.message.from_user.id != int(admin_id):
        await update.message.reply_text("У вас нет прав на выполнение этой команды.")
        return

    # Загружаем чаты
    chats = load_chats()
    all_user_ids = {}  # Инициализируем словарь для хранения ID пользователей по чатам

    bot = Bot(token=bot_token)

    # Перебираем все чаты, чтобы собрать ID пользователей
    for chat_id in chats.keys():
        try:
            # Получаем администраторов чата
            administrators = await bot.get_chat_administrators(chat_id)
            if chat_id not in all_user_ids:
                all_user_ids[chat_id] = set()  # Инициализируем множество для чата

            for admin in administrators:
                all_user_ids[chat_id].add(admin.user.id)  # Добавляем ID администратора
        except Exception as e:
            await update.message.reply_text(f"Не удалось получить администраторов чата {chat_id}: {e}")
            continue

    # Сохраняем все собранные ID пользователей в файл
    save_user_ids(all_user_ids)
    await update.message.reply_text(f"ID пользователей успешно собраны и сохранены.")




# Функция для обработки добавления бота в чат
async def handle_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_title = update.effective_chat.title
    chat_type = update.effective_chat.type

    # Проверяем статус бота
    if update.my_chat_member.new_chat_member.status in ['member', 'administrator']:
        logger.info(f"Бот добавлен в чат: {chat_id}, {chat_title}")

        # Загружаем текущие чаты
        chats = load_chats()

        # Добавляем чат в список, если его ещё нет
        if str(chat_id) not in chats:
            chats[str(chat_id)] = {
                "chat_name": chat_title,
                "chat_type": chat_type
            }
            save_chats(chats)
            logger.info(f"Чат {chat_id} добавлен в список.")
        else:
            logger.info(f"Чат {chat_id} уже существует.")



# Функция для отслеживания сообщений пользователей и записи их ID
async def track_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Получаем ID пользователя, который отправил сообщение
    chat_id = update.effective_chat.id  # Получаем ID чата

    # Логируем ID пользователя
    logger.info(f"Пользователь с ID {user_id} отправил сообщение в чат {chat_id}")

    # Загружаем текущий список пользователей
    if chat_id not in user_ids_dict:
        user_ids_dict[chat_id] = set()  # Используем set для уникальности пользователей

    # Добавляем ID пользователя в set, если его нет в списке
    user_ids_dict[chat_id].add(user_id)

    # Логируем обновленный список пользователей
    logger.info(f"Обновленный список пользователей для чата {chat_id}: {user_ids_dict[chat_id]}")

    # Сохраняем обновленный список ID пользователей в файл
    save_user_ids(user_ids_dict)




# Основная функция для запуска бота
def main():
    application = Application.builder().token(bot_token).build()

    # Обработчик команды /kick для удаления пользователя
    application.add_handler(CommandHandler("kick", kick_user))

    # Обработчик команды /collect_user_ids для сбора всех ID пользователей
    application.add_handler(CommandHandler("collect_user_ids", collect_user_ids))

    # Обработчик для отслеживания добавления новых пользователей
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_new_user))

     # Обработчик для добавления чата при добавлении бота
    application.add_handler(ChatMemberHandler(handle_bot_added))

    # Обработчик для отслеживания сообщений пользователей
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
