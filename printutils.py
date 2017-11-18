import discord

def lineBreak():
    print('---------------------------------')

def printServers(client):
    tmp = ""
    for server in client.servers:
        tmp += server.name
    print("Available servers: " + tmp)

def printUser(client):
    print('Logged in as: ' + client.user.name)

def printChannels(server):
    print("Available channels:")
    lineBreak();
    for channel in  server.channels:
        print(channel.name)
