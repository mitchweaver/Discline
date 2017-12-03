# Wrapper class to make dealing with logs easier

class ChannelLog():

    __name = ""
    __logs = ""
    __server_name = ""
    unread = False

    def __init__(self, server_name, name, logs):
        self.__name = name
        self.__logs = logs
        self.__server_name = server_name

    def get_logs(self):
        return self.__logs

    def get_name(self):
        return self.__name

    def get_server_name(self):
        return self.__server_name

    def append(self, message):
        self.__logs.append(message)

    def index(self, message):
        return self.__logs.index(message)

    def insert(self, i, message):
        self.__logs.insert(i, message)
