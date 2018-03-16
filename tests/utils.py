class User:
    def __init__(self, name):
        self.name = name
        self.nick = name

class Message:
    def __init__(self, author, content):
        self.author = author
        self.content = content
