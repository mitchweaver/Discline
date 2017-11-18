import discord
import curses
import asyncio
import sys
from printutils import *
from client import client

# await client.login('zemajujo@axsup.net', 'testpassword')

token = sys.argv[1]
client = client(max_messages=100)
servers = []
prefix = '/'

currentServer="DisKvlt"
currentChannel="terminal_discord"

####### INITIALIZATION ################################################
def initServers():
    global servers
    servers = []
    for server in client.servers:
        servers.append(server)
#######################################################################

@client.async_event
async def on_ready(): 
    print("Client is starting...")
    client.wait_until_login()
    if client.is_logged_in:
        print("Client has logged in successfully!")
    else:
        print("Error: Login failed")
        quit()
    print("Initializing...")
    initServers()
    lineBreak()
    printUser(client)
    printServers(client)
    lineBreak()

    while True:
        a = input("terminal_discord: ")
        await client.send_message(client.getChannel("terminal_discord"), a)
                              
                              
client.run(token, bot=False)
