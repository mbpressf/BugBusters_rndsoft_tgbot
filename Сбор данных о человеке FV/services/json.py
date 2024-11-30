import json

class JSON:
    def __init__(self, filepath):
        self.filepath = filepath

    def save(self, data):
        # Сохраняем данные в файл JSON
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
