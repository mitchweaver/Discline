# Wrapper class to make dealing with logs easier

import os

LIMITED_LOGS = True

def formatlog(loglist):
    convertime = lambda t: t.ctime().split(" ")[-2]
    currauthor = None
    buff = str()
    for message in loglist:
        if not currauthor or str(message.author.display_name) != currauthor:
            currauthor = str(message.author.display_name)
            buff += "\n{}:\n".format(currauthor)
        buff += "\t{}| {}\n".format(convertime(message.timestamp), message.content)
    return buff

def getdiff(old_data, new_data):
    crossed = False
    oldhead = None
    newhead = None
    cross = 0
    old_list = [(i, l) for i, l in enumerate(old_data.split("\n")) if "|" in l]
    new_list = [(i, l) for i, l in enumerate(new_data.split("\n")) if "|" in l]
    for line in new_list:
        if line[1] in [el[1] for el in old_list]:
            nl = [el[1] for el in new_list].index(line[1])  #1 not in list
            ol = [el[1] for el in old_list].index(line[1])
            if ol != nl:
                oldhead = ol < nl
                newhead = ol > nl
            if newhead: cross = line[0]
            elif oldhead: cross = old_list[ol][0]

    if not crossed or not oldhead or not newhead:
        return new_data
    elif oldhead:
        return "\n".join(old_data.split("\n")[:cross] + new_data)
    else:
        return "\n".join(new_data.split("\n")[:cross] + old_data)

class ChannelLog():

    __channel = ""
    __logs = []
    unread = False
    mentioned_in = False
    # the index of where to start printing the messages
    __index = 0

    def __init__(self, channel, logs):
        self.__channel = channel
        self.__logs = list(logs)
        self.log_save = ".chan_{}_log".format(channel)
        self.last_update = 0

    def get_server(self): return self.__channel.server
    def get_channel(self): return self.__channel

    def get_logs(self):
        self.update_log()
        return self.__logs

    def get_name(self):
        return self.__channel.name

    def get_server_name(self):
        return self.__channel.server.name

    def append(self, message):
        self.__logs.append(message)

    def index(self, message):
        return self.__logs.index(message)

    def insert(self, i, message):
        self.__logs.insert(i, message)

    def len(self):
        return len(self.__logs)

    def get_index(self):
        return self.__index

    def set_index(self, int):
        self.__index = int

    def inc_index(self, int):
        self.__index += int

    def dec_index(self, int):
        self.__index -= int

    def update_log(self):
        if hash(str(self.__logs)) != self.last_update:
            self.last_update = hash(str(self.__logs))
            if os.path.isfile(self.log_save) and not LIMITED_LOGS:
                with open(self.log_save, "r") as fichier:
                    odata = fichier.read()
            else:
                odata = ""
            with open(self.log_save, "w") as fichier:
                fichier.write(getdiff(odata, formatlog(self.__logs)))
