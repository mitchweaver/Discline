import discord
from utils.globals import gc
from utils.settings import settings
import ui.text_manipulation as tm

# inherits from discord.py's Client
class Client(discord.Client):

    # NOTE: These are strings!
    __current_server = ""
    __current_channel = ""
    __prompt = ""

    # discord.Status object
    __status = ""

    # discord.Game object
    __game = ""


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
        for server in self.servers:
            if server.name.lower() == self.__current_server:
                return server

    def get_current_server_log(self):
        for slog in gc.server_log_tree:
            if slog.get_server() == self.get_current_server():
                return slog

    def get_current_channel(self):
        for server in self.servers:
            if server.name.lower() == self.__current_server.lower():
                for channel in server.channels:
                    if channel.type is discord.ChannelType.text:
                        if channel.name.lower() == self.__current_channel.lower():
                            if channel.permissions_for(server.me).read_messages:
                                return channel

    async def populate_current_channel_log(self):
        slog = self.get_current_server_log()
        for idx, clog in enumerate(slog.get_logs()):
            if clog.get_channel().type is discord.ChannelType.text:
                if clog.get_channel().name.lower() == self.__current_channel.lower():
                    if clog.get_channel().permissions_for(slog.get_server().me).read_messages:
                        async for msg in self.logs_from(clog.get_channel(), limit=settings["max_log_entries"]):
                            clog.insert(0, await tm.calc_mutations(msg))

    def get_current_channel_log(self):
        slog = self.get_current_server_log()
        for idx, clog in enumerate(slog.get_logs()):
            if clog.get_channel().type is discord.ChannelType.text:
                if clog.get_channel().name.lower() == self.__current_channel.lower():
                    if clog.get_channel().permissions_for(slog.get_server().me).read_messages:
                        return clog

    # returns online members in current server
    async def get_online(self):
        online_count = 0
        if not self.get_current_server() == None:
            for member in self.get_current_server().members:
                if member is None: continue # happens if a member left the server
                if member.status is not discord.Status.offline:
                    online_count +=1
            return online_count

    # because the built-in .say is really buggy, just overriding it with my own
    async def say(self, string):
        await self.send_message(self.get_current_channel(), string)

    async def set_game(self, string):
        self.__game = discord.Game(name=string,type=0)
        self.__status = discord.Status.online
        # Note: the 'afk' kwarg handles how the client receives messages, (rates, etc)
        # This is meant to be a "nice" feature, but for us it causes more headache
        # than its worth.
        if self.__game is not None and self.__game != "":
            if self.__status is not None and self.__status != "":
                try: await self.change_presence(game=self.__game, status=self.__status, afk=False)
                except: pass
            else:
                try: await self.change_presence(game=self.__game, status=discord.Status.online, afk=False)
                except: pass

    async def get_game(self):
        return self.__game

    async def set_status(self, string):
        if string == "online":
            self.__status = discord.Status.online
        elif string == "offline":
            self.__status = discord.Status.offline
        elif string == "idle":
            self.__status = discord.Status.idle
        elif string == "dnd":
            self.__status = discord.Status.dnd

        if self.__game is not None and self.__game != "":
            try: await self.change_presence(game=self.__game, status=self.__status, afk=False)
            except: pass
        else:
            try: await self.change_presence(status=self.__status, afk=False)
            except: pass

    async def get_status(self):
        return self.__status
