class State():

    __state = ""

    def set_channel_log(self):
        self.__state = "channel_log"

    def set_help(self):
        self.__state = "help"

    def set_servers(self):
        self.__state = "servers"

    def set_channels(self):
        self.__state = "channels"

    def set_welcome(self):
        self.__state = "welcome"



    def is_channel_log(self):
        return self.__state == "channel_log"

    def is_help(self): 
        return self.__state == "help"

    def is_servers(self):
        return self.__state == "servers"

    def is_channels(self):
        return self.__state == "channels"

    def is_welcome(self):
        return self.__state == "welcome"
