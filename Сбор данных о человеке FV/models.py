import json

class User:
    def __init__(self, id, username, first_name, last_name):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

class Message:
    def __init__(self, id, text, date):
        self.id = id
        self.text = text
        self.date = date