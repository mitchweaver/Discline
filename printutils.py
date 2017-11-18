import discord
import os

def lineBreak():
    print('---------------------------------')

<<<<<<< HEAD
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

=======
>>>>>>> 0b187ac... goalpost: message sending
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
