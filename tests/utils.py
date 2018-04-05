class Role:
    def __init__(self, name):
        self.name = name

class User:
    def __init__(self, name, top_role):
        self.name = name
        self.nick = name
        self.top_role = top_role

class Message:
    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.clean_content = content
