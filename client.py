import discord

# inherits from discord.py's Client
class client(discord.Client):

    # NOTE: These are strings!
    __current_server=""
    __current_channel=""
    __prompt=""

    def getChannel(self, string):
        return discord.utils.find(lambda c: c.name == string, self.get_all_channels())

    def getServer(self, string):
        return discord.utils.find(lambda s: s.name == string, self.servers)


    
    # Note: setting only allows for string types
    def setPrompt(self, string): self.__prompt = string
    def setCurrentServer(self, string): self.__current_server = string
    def setCurrentChannel(self, string): self.__current_channel = string
    
    def getPrompt(self): return self.__prompt
    def getCurrentServerName(self): return self.__current_server
    def getCurrentChannelName(self): return self.__current_channel

    def getCurrentServer(self): return self.getServer(self.__current_server)
    def getCurrentChannel(self): return self.getChannel(self.__current_channel)
