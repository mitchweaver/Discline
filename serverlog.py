from discord import Server, Channel
from channellog import ChannelLog

# Simple wrapper class to hold a list of ChannelLogs

class ServerLog():

    __server = ""
    __name = ""
    __channel_logs = []

    def __init__(self, server, channel_log_list):
        self.__server = server
        self.__name = server.name
        self.__channel_logs = channel_log_list

    def get_server(self):
        return self.__server

    def get_name(self):
        return self.__name

    def get_logs(self):
        return self.__channel_logs

    def clear_logs(self):
        for channel_log in self.__channel_logs:
            del channel_log[:]

    def add_logs(self, log_list):
        for logs in log_list:
            self.__channel_logs.append(logs)
