import discord
import curses
import asyncio
import sys
import os
from printutils import *
from client import client
from help import *

# await client.login('zemajujo@axsup.net', 'testpassword')

token = sys.argv[1]
client = client(max_messages=100)
servers = []
prefix = '/'

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
    client.setPrompt("[ ~ ]: ")
    client.setCurrentServer("DisKvlt")
    client.setCurrentChannel("terminal_discord")

    await client.logs_from(client.getCurrentChannel)


    while True:
        lineBreak()
        # Prompt user for input
        user_input = input(client.getPrompt())
        
        # Strip trailing white space, (if any)
        user_input = user_input.rstrip()
        
        # If input is blank, don't do anything
        if user_input == '': continue

        # Check if input is a command
        if user_input[0] == prefix:
            # Strip the prefix
            user_input = user_input[1:]

            # Check if contains a space
            if ' ' in user_input:
                # Split into command and argument
                command,arg = user_input.split(" ", 1)
                if command == "server":
                    # TODO: check if arg is a valid server
                    client.setCurrentServer(arg)
                    clearScreen()
                    lineBreak()
                    print("Joined server: " + client.getCurrentServerName())
                    lineBreak()
                elif command == "channel":
                    # TODO: check if arg is a valid channel
                    client.setCurrentChannel(arg)
                    client.setPrompt("[ " + arg + " ]: ")
            # Else we must have only a command, no argument
            else:
                command = user_input
                if command == "help": printHelp()
                if command == "clear": clearScreen()
        
        # This must not be a command...
        else: 
            # If all options have been exhausted, it must be chat
            await client.send_message(client.getCurrentChannel, arg)
                             

client.run(token, bot=False)
