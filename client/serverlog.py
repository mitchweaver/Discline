from discord import Server, Channel
from client.channellog import ChannelLog

# Simple wrapper class to hold a list of ChannelLogs
class ServerLog():

    __server = ""
    __channel_logs = []

    def __init__(self, server, channel_log_list):
        self.__server = server
        self.__channel_logs = list(channel_log_list)

    def get_server(self):
        return self.__server

    def get_name(self):
        return self.__server.name

    def get_logs(self):
        return self.__channel_logs

    def clear_logs(self):
        for channel_log in self.__channel_logs:
            del channel_log[:]

    # takes list of ChannelLog
    def add_logs(self, log_list):
        for logs in log_list:
            self.__channel_logs.append(logs)
