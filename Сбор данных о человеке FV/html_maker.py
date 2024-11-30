import json

# Чтение данных из файла data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Получаем информацию о пользователе
user_info = data.get('user_info', 'Информация о пользователе отсутствует')

# Формируем HTML строку
html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Messages</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .container {{
            width: 80%;
            margin: 20px auto;
            background-color: white;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }}
        h1 {{
            color: #4CAF50;
            text-align: center;
        }}
        .user-info {{
            margin-top: 20px;
        }}
        .user-info table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .user-info th, .user-info td {{
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        .user-info th {{
            background-color: #f2f2f2;
        }}
        .message {{
            background-color: #e1f5fe;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }}
        .message:hover {{
            background-color: #b3e5fc;
        }}
        .message-text {{
            font-size: 1em;
            color: #333;
        }}
        .message-info {{
            display: none;
            margin-top: 10px;
            font-size: 0.9em;
            color: #616161;
        }}
    </style>
    <script>
        function toggleMessageInfo(messageId) {{
            var messageInfo = document.getElementById(messageId);
            if (messageInfo.style.display === "none" || messageInfo.style.display === "") {{
                messageInfo.style.display = "block";
            }} else {{
                messageInfo.style.display = "none";
            }}
        }}
    </script>
</head>
<body>

    <div class="container">
        <h1>User Information</h1>
        
        <div class="user-info">
            <table>
                <tr>
                    <th>ID</th>
                    <td>{user_info.get('id', 'Не указано')}</td>
                </tr>
                <tr>
                    <th>First Name</th>
                    <td>{user_info.get('first_name', 'Не указано')}</td>
                </tr>
                <tr>
                    <th>Username</th>
                    <td>{user_info.get('username', 'Не указано')}</td>
                </tr>
                <tr>
                    <th>Type</th>
                    <td>{user_info.get('type', 'Не указано')}</td>
                </tr>
                <tr>
                    <th>Active Usernames</th>
                    <td>{', '.join(user_info.get('active_usernames', ['Не указано']))}</td>
                </tr>
                <tr>
                    <th>Has Private Forwards</th>
                    <td>{user_info.get('has_private_forwards', 'Не указано')}</td>
                </tr>
                <tr>
                    <th>Max Reaction Count</th>
                    <td>{user_info.get('max_reaction_count', 'Не указано')}</td>
                </tr>
                <tr>
                    <th>Accent Color ID</th>
                    <td>{user_info.get('accent_color_id', 'Не указано')}</td>
                </tr>
                <tr>
                    <th>Background Custom Emoji ID</th>
                    <td>{user_info.get('background_custom_emoji_id', 'Не указано')}</td>
                </tr>
            </table>
        </div>

        <h2>Messages</h2>
        <div>
"""

# Добавление сообщений
for idx, message in enumerate(data.get('messages', [])):
    text = message.get('text', '[Пустое сообщение]')
    date = message.get('date', 'Дата не указана')
    time = message.get('time', 'Время не указано')

    # Уникальный ID для каждого сообщения
    message_id = f"message_{idx}"

    html_content += f"""
        <div class="message" onclick="toggleMessageInfo('{message_id}')">
            <div class="message-text">
                {text}
            </div>
            <div id="{message_id}" class="message-info">
                <p><strong>Дата:</strong> {date}</p>
                <p><strong>Время:</strong> {time}</p>
            </div>
        </div>
    """

# Закрытие HTML
html_content += """
    </div>
</body>
</html>
"""

# Сохранение HTML в файл
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML файл успешно создан и сохранён как 'output.html'")
