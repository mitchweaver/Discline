import discord

# inherits from discord.py's Client
class client(discord.Client):

    def getChannel(self, string):
        return discord.utils.find(lambda c: c.name == string, self.get_all_channels())

    def getServer(self, string):
        return discord.utils.find(lambda s: s.name == string, self.servers)
