import discord
import asyncio
import sys
import os
from printutils import *
from client import client
from help import *
import ui

# await client.login('zemajujo@axsup.net', 'testpassword')

token = sys.argv[1]
client = client(max_messages=300)
prefix = '/'

@client.event
async def on_ready(): 
    # print("Client is starting...")
    client.wait_until_login()
    # if client.is_logged_in:
        # print("Client has logged in successfully!")
    # else:
        # print("Error: Login failed")
        # quit()
    # lineBreak()
    # printUser(client)
    # printServers(client)
    client.setPrompt("[ ~ ]: ")
    client.setCurrentServer("DisKvlt")
    client.setCurrentChannel("terminal_discord")

    client.setPrompt("~")

    # Print initial screen
    ui.printScreen(client, None)

    while True:
        messages = client.messages
        # for m in messages: print(m.content)

        # Clear channel log
        channelLog = []

        # Prompt user for input
        # user_input = input()

        from blessings import Terminal

        term = Terminal()
        # Note: input() needs to be set at 1 line higher than the prompt
        with term.location(len(client.getPrompt()) + 7, term.height - 2):
            user_input = input()

        
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
                    client.setCurrentChannel(client.getServer(arg).default_channel)
                    ui.clearScreen()
                    lineBreak()
                    # print("Joined server: " + client.getCurrentServerName())
                    lineBreak()
                elif command == "channel":
                    # TODO: check if arg is a valid channel
                    client.setCurrentChannel(arg)
                    client.setPrompt(arg)
            
                    async for msg in client.logs_from(client.getCurrentChannel(), limit=30):
                        channelLog.insert(0, msg)

            # Else we must have only a command, no argument
            else:
                command = user_input
                if command == "help": printHelp()
                if command == "clear": ui.clearScreen()
        
        # This must not be a command...
        else: 
            # If all options have been exhausted, it must be chat
            await client.send_message(client.getCurrentChannel(), user_input)

        # Update the screen
        ui.printScreen(client, channelLog)
                             

client.run(token, bot=False)
