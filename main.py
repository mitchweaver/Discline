import discord
#import curses
import asyncio

# max_messages can be edited to your liking
client = discord.Client(max_messages=10000)

# The leading character for commands
prefix = '/'

servers = []



######## PRINTING UTILS ############################################
def lineBreak():
    print('---------------------------------') 

def printServers():
    tmp = ""
    for server in servers:
        tmp += server.name
    print("Available servers: " + tmp)

def printUser():
    print('Logged in as: ' + client.user.name)

def printChannels(server):
    print("Available channels:")
    lineBreak();
    for channel in  server.channels:
        print(channel.name)
    print();

###### INITIALIZATION ################################################
def initServers():
    global servers
    servers = []
    for server in client.servers:
        servers.append(server)

######################################################################

@client.event
async def on_ready(): 
    print("Client is starting...")
    await client.login('zemajujo@axsup.net', 'testpassword')
    print("Client has logged in successfully!")
    print("Initializing...")
    initServers()
    lineBreak()
    printUser()
    printServers()
    lineBreak()
    printChannels(servers[0])
    lineBreak()

client.run(token, bot=False)
