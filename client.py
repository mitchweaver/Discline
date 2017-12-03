import discord

# inherits from discord.py's Client
class Client(discord.Client):

    # NOTE: These are strings!
    __current_server = ""
    __current_channel = ""
    __prompt = ""
    
    def get_channel(self, string):
        return discord.utils.find(lambda c: c.name == string, \
                                  self.get_all_channels())

    def get_server(self, string):
        return discord.utils.find(lambda s: s.name == string, self.servers)


    # Note: setting only allows for string types
    def set_prompt(self, string): self.__prompt = string
    def set_current_server(self, string): self.__current_server = string
    def set_current_channel(self, string): self.__current_channel = string

    def get_prompt(self): return self.__prompt
    def get_current_server_name(self): return self.__current_server
    def get_current_channel_name(self): return self.__current_channel

    def get_current_server(self): return self.get_server(self.__current_server)
    def get_current_channel(self): return self.get_channel(self.__current_channel)


    # returns online members in current server
    def get_online(self):
        online_count = 0
        for member in self.get_current_server().members:
            if member is None: continue # happens if a member left the server
            if member.status is discord.Status.online:
                online_count +=1 
        return online_count

