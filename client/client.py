import discord
import utils.globals

# inherits from discord.py's Client
class Client(discord.Client):

    # NOTE: These are strings!
    __current_server = ""
    __current_channel = ""
    __prompt = ""
    
    # Note: setting only allows for string types
    def set_prompt(self, string): 
        self.__prompt = string.lower()
    def set_current_server(self, string): 
        self.__current_server = string.lower()
    def set_current_channel(self, string): 
        self.__current_channel = string.lower()
        self.set_prompt(string)

    def get_prompt(self): return self.__prompt
    def get_current_server_name(self): return self.__current_server
    def get_current_channel_name(self): return self.__current_channel

    def get_current_server(self):
        if self.__current_server is None:
            print(globals.term.red + "Current server is None!" + globals.term.normal)
            return
        for server in self.servers:
            if server.name.lower() == self.__current_server:
                return server

    def get_current_channel(self): 
        if self.__current_channel is None:
            print(globals.term.red + "Current channel is None!" + globals.term.normal)
            return
        for server in self.servers:
            if server.name.lower() == self.__current_server.lower():
                for channel in server.channels:
                    if channel.type is discord.ChannelType.text:
                        if channel.name.lower() == self.__current_channel.lower():
                            if channel.permissions_for(server.me).read_messages:
                                return channel

    def get_current_channel_log(self):
        if self.__current_channel is None:
            print(globals.term.red + "Current channel is None!" + globals.term.normal)
            return
        for slog in server_log_tree:
            if slog.get_server() == self.get_current_server():
                for clog in slog.get_logs():
                    if clog.get_channel().type is discord.ChannelType.text:
                        if clog.get_channel().name.lower() == self.__current_channel.lower():
                            if clog.get_channel().permissions_for(slog.get_server().me).read_messages:
                                return clog.get_channel()


    # returns online members in current server
    async def get_online(self):
        online_count = 0
        for member in self.get_current_server().members:
            if member is None: continue # happens if a member left the server
            if member.status is discord.Status.online:
                online_count +=1 
        return online_count

    # because the built-in .say is really buggy, just overriding it with my own
    async def say(self, string):
        await self.send_message(self.get_current_channel(), string)
