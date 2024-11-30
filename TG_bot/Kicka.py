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
admin_ids = {7004441787, 5405355475}  # Используем множество для уникальности



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












import re

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы MarkdownV2."""
    text = re.sub(r'([\\`*_{}[\]()#+\-.!_])', r'\\\1', text)  # Экранируем обычные специальные символы
    text = text.replace('(', r'\(').replace(')', r'\)')  # Экранируем круглые скобки
    return text

import time
from httpx import ConnectError

# async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Проверка, что команда пришла от администратора
#     if update.message.from_user.id not in admin_ids:
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
#         attempts = 3  # Количество попыток
#         for attempt in range(attempts):
#             try:
#                 bot = Bot(token=bot_token)
#                 administrators = await bot.get_chat_administrators(chat_id)

#                 # Проверяем, является ли отправитель команды администратором в этом чате
#                 if update.message.from_user.id not in [admin.user.id for admin in administrators]:
#                     # await update.message.reply_text(f"Вы не являетесь администратором в чате {chat_id}.")
#                     break  # Прерываем выполнение, если ошибка связана с правами администратора

#                 # Получаем информацию о пользователе
#                 user = await bot.get_chat_member(chat_id, user_id)
#                 user_name = user.user.username if user.user.username else f"{user.user.first_name} {user.user.last_name}"
#                 user_status = user.status  # Статус пользователя в чате

#                 # Если пользователь не забанен, пытаемся получить дату присоединения
#                 user_joined = 'Неизвестно'
#                 if user_status != 'banned' and hasattr(user, 'joined_date') and user.joined_date:
#                     user_joined = user.joined_date.strftime('%Y-%m-%d %H:%M:%S')

#                 # Получаем имя чата и другую информацию
#                 chat_name = chat_info.get('chat_name', 'Неизвестный чат')
#                 chat_title = await bot.get_chat(chat_id)  # Для получения дополнительных данных о чате
#                 chat_type = chat_title.type  # Тип чата: канал, группа, супергруппа и т.д.
#                 chat_description = chat_title.description if chat_title.description else 'Нет описания'

#                 # Экранируем специальные символы в именах пользователя и чата
#                 user_name = escape_markdown_v2(user_name)
#                 chat_name = escape_markdown_v2(chat_name)

#                 # Если отправитель является администратором, удаляем пользователя
#                 await bot.ban_chat_member(chat_id, user_id)  # Используем ban_chat_member

#                 # Формируем сообщение с использованием MarkdownV2 и скрытия текста
#                 message = (
#                     f"Пользователь: @{user_name} \(ID: ||\{user_id}||\)\n"
#                     f"Статус в чате: {user_status}\n"
#                     f"Дата присоединения: {user_joined}\n\n"
#                     f"Чат: {chat_name} \(ID: ||\{chat_id}||\)\n"
#                     f"Тип чата: {chat_type}\n"
#                     f"Описание чата: {chat_description}\n\n"
#                     f"Пользователь был удален из чата"
#                 )

#                 # Отправляем сообщение в формате MarkdownV2
#                 await update.message.reply_text(message, parse_mode='MarkdownV2')

#                 break  # Прерываем цикл повторных попыток, если операция выполнена успешно

#             except ConnectError as e:
#                 if attempt < attempts - 1:
#                     await update.message.reply_text(f"Ошибка подключения, повторная попытка через 3 секунды... ({attempt + 1}/{attempts})")
#                     time.sleep(3)  # Задержка между попытками
#                 else:
#                     await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")
#             except Exception as e:
#                 await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")






def save_removed_user(user_id, user_name, user_status, removed_from_chats):
    try:
        # Загружаем текущие удалённые пользователи
        try:
            with open('users_ids_rm.json', 'r', encoding='utf-8') as file:
                removed_users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            removed_users = {}

        # Проверяем, был ли этот пользователь уже удалён
        if str(user_id) not in removed_users:
            removed_users[str(user_id)] = {
                'name': user_name,
                'status': user_status,
                'removed_from_chats': removed_from_chats
            }

            # Сохраняем обновленный файл
            with open('users_ids_rm.json', 'w', encoding='utf-8') as file:
                json.dump(removed_users, file, ensure_ascii=False, indent=4)
            logger.info(f"Пользователь {user_id} добавлен в файл удалённых пользователей.")
        else:
            # Если пользователь уже есть, то обновляем его данные
            removed_users[str(user_id)]['removed_from_chats'].extend(removed_from_chats)

            # Убираем дубликаты в списке удалённых чатов
            removed_users[str(user_id)]['removed_from_chats'] = [
                dict(t) for t in {tuple(d.items()) for d in removed_users[str(user_id)]['removed_from_chats']}
            ]

            # Сохраняем обновленный файл
            with open('users_ids_rm.json', 'w', encoding='utf-8') as file:
                json.dump(removed_users, file, ensure_ascii=False, indent=4)
            logger.info(f"Данные о пользователе {user_id} обновлены.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении удалённого пользователя {user_id}: {e}")



# Функция для удаления пользователя из user_ids.json и добавления в users_ids_rm.json
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что команда пришла от администратора
    if update.message.from_user.id not in admin_ids:
        await update.message.reply_text("У вас нет прав на выполнение этой команды.")
        return

    # Получаем ID пользователя и ID чатов из аргументов команды
    try:
        user_id = int(context.args[0])  # ID пользователя, которого нужно удалить
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста, укажите ID пользователя для удаления.")
        return

    # Загружаем чаты и список пользователей
    chats = load_chats()
    
    removed_from_chats = []  # Список чатов, из которых был удалён пользователь

    bot = Bot(token=bot_token)

    # Перебираем все чаты, чтобы проверить, является ли отправитель администратором
    for chat_id, chat_info in chats.items():
        attempts = 3  # Количество попыток
        for attempt in range(attempts):
            try:
                administrators = await bot.get_chat_administrators(chat_id)

                # Проверяем, является ли отправитель команды администратором в этом чате
                if update.message.from_user.id not in [admin.user.id for admin in administrators]:
                    break  # Прерываем выполнение, если ошибка связана с правами администратора

                # Получаем информацию о пользователе
                user = await bot.get_chat_member(chat_id, user_id)
                user_name = user.user.username if user.user.username else f"{user.user.first_name} {user.user.last_name}"
                user_status = user.status  # Статус пользователя в чате

                # Блокируем пользователя
                await bot.ban_chat_member(chat_id, user_id)  # Используем ban_chat_member

                # Добавляем информацию о чате в список удалённых
                removed_from_chats.append({
                    'name': chat_info['chat_name'],
                    'id': chat_id,
                    'type': chat_info['chat_type']
                })



                print("userdict =",user_ids_dict, '\n')
                print(type(chat_id))
                print(type(list(user_ids_dict.keys())[0]))

                # Удаляем пользователя из списка пользователей этого чата
                chat_id = int(chat_id)

                if chat_id in user_ids_dict:
                    print(f"удаляем{user_id}из{chat_id}, \n\n")
                    user_ids_dict[chat_id].discard(user_id)


                # Если пользователь не забанен, пытаемся получить дату присоединения
                user_joined = 'Неизвестно'
                if user_status != 'banned' and hasattr(user, 'joined_date') and user.joined_date:
                    user_joined = user.joined_date.strftime('%Y-%m-%d %H:%M:%S')



                # Получаем имя чата и другую информацию
                chat_name = chat_info.get('chat_name', 'Неизвестный чат')
                chat_title = await bot.get_chat(chat_id)  # Для получения дополнительных данных о чате
                chat_type = chat_title.type  # Тип чата: канал, группа, супергруппа и т.д.
                chat_description = chat_title.description if chat_title.description else 'Нет описания'
                chat_username = chat_title.username  # Получаем username чата
                
                
                
                # Проверка на наличие username
                if chat_username:
                    chat_url = f"https://t.me/{chat_username}"
                else:
                    chat_url = f"ID чата: {chat_id}"  # Просто выводим ID чата, если нет username

                message = (
                    f"Пользователь: @{user_name} \(ID: ||\{user_id}||\)\n"
                    f"Статус в чате: {user_status}\n"
                    f"Дата присоединения: {user_joined}\n\n"
                    f"Чат: [{chat_name}]({chat_url}) \(ID: ||\{chat_id}||\)\n"
                    f"Тип чата: {chat_type}\n"
                    f"Описание чата: {chat_description}\n\n"
                    f"Пользователь был удален из чата"
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
            except Exception as e:
                await update.message.reply_text(f"Не удалось удалить пользователя из чата {chat_id}: {e}")

    # Сохраняем обновлённый список пользователей
    print("бубубу",user_ids_dict)
    save_user_ids(user_ids_dict)

    # Сохраняем информацию о удалённом пользователе
    print(user_id, user_name, user_status, removed_from_chats)
    save_removed_user(user_id, user_name, user_status, removed_from_chats)

    # Отправляем уведомление о завершении операции
    await update.message.reply_text(f"Пользователь {user_name} был удалён из чатов.")

















# Функция для сбора всех ID пользователей из всех чатов
async def collect_user_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что команда пришла от администратора
    if update.message.from_user.id not in admin_ids:
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


import httpx
import ssl

# Пример настройки для игнорирования SSL ошибок (для тестирования)
client = httpx.Client(verify=False)



if __name__ == '__main__':
    main()
