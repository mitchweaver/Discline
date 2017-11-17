import discord
import curses
import asyncio
import sys
from printutils import *

# await client.login('zemajujo@axsup.net', 'testpassword')

token = sys.argv[1]
client = discord.Client(max_messages=10000)
servers = []
prefix = '/'

current_server=""
current_channel=""

####### INITIALIZATION ################################################
def initServers():
    global servers
    servers = []
    for server in client.servers:
        servers.append(server)
#######################################################################

@client.event
async def on_ready(): 
    print("Client is starting...")
    print("Client has logged in successfully!")
    print("Initializing...")
    initServers()
    lineBreak()
    printUser(client)
    printServers(client)
    lineBreak()
    printChannels(servers[0])
    lineBreak()

    
    


client.run(token, bot=False)
