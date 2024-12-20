# Описание файлов проекта

## Главные файлы

### `main.py`
Точка входа в проект. Запускает бота, передавая необходимые параметры, такие как `user_id` и `chat_id`. Обеспечивает взаимодействие между модулями.

### `bot.py`
Основной логический модуль бота. Отвечает за сбор данных о пользователе, извлечение сообщений из чатов, их обработку и сохранение в JSON.

---

## Модули в папке `services/`

### `tg_api.py`
Модуль для работы с Telegram API. Обеспечивает взаимодействие с чатами и пользователями: извлекает информацию о профиле и сообщения.

### `my_json.py`
Модуль для работы с JSON-файлами. Содержит функции сохранения и загрузки данных в/из файлов.

---

## Пример данных

### `data.json`
Файл, в который сохраняется собранная информация о пользователе и его сообщениях. Данные включают:
- Информацию о профиле пользователя.
- Список сообщений с датой, временем и текстом.
- Аналитику по сообщениям (опционально).

---

## Прочее

### `config.py`
Конфигурационный файл. Содержит настройки проекта, такие как токен бота, пути к данным и другие параметры.

### `models.py`
Определяет структуры данных, используемых в проекте. Например, может содержать модели для профиля пользователя или сообщения.

### `test.py`
Скрипт для тестирования функциональности бота. Проверяет корректность работы модулей и их взаимодействие.
