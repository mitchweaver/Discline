# Wrapper class to make dealing with logs easier

class ChannelLog():

    __server = ""
    __channel = ""
    __name = ""
    __logs = ""
    __server_name = ""
    unread = False

    def __init__(self, server, channel, logs):
        self.__server = server
        self.__channel = channel
        self.__name = channel.name
        self.__logs = logs
        self.__server_name = server.name

    def get_server(self): return self.__server
    def get_channel(self): return self.__channel

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
