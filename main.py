import sys
import discord
from printutils import *
from settings import *
from client import Client
from help import *
import ui
import terminalinput
from threading import Thread
import asyncio
from time import sleep
from serverlog import ServerLog
from channellog import ChannelLog

# await client.login('zemajujo@axsup.net', 'testpassword')

message_to_send = ""
user_input = ""

@client.event
async def on_ready():
    client.wait_until_login()

    # these values are set in settings.py
    if DEFAULT_PROMPT is not None:
        client.set_prompt(DEFAULT_PROMPT)
    else: client.set_prompt('~')

    if DEFAULT_SERVER is not None:
        client.set_current_server(DEFAULT_SERVER)
        if DEFAULT_CHANNEL is not None:
            client.set_current_channel(DEFAULT_CHANNEL)


# --------------- INIT SERVERS --------------------------------------------- #
    print("Loading channels...")

    logs = []
    # if the server has already been added,
    # just refresh the log list
    # for server_log in server_log_tree:
    #     if server_log.get_name() == server.name:
    #         server_log.clear_logs()
    #         for channel in server.channels:
    #             channel_log = []
    #             async for msg in client.logs_from(channel, limit=MAX_LOG_ENTRIES):
    #                 channel_log.insert(0, msg)
    #             logs.append(channel_log)
    #         return
 
    count = 0
    # if we're still here, the server must be new to us
    for server in client.servers:
        print("loading " + server.name + " ...")
        for channel in server.channels:
            print("    loading " + channel.name)
            channel_log = []
            try:
                async for msg in client.logs_from(channel, limit=MAX_LOG_ENTRIES):
                    count+=1
                    channel_log.insert(0, msg)
                logs.append(ChannelLog(server.name, channel.name, channel_log))
            except:
                # https forbidden exception, you don't have priveleges for
                # this channel!
                continue

        # add it to the tree
        server_log_tree.append(ServerLog(server.name, logs)) 

    print("Channels loaded! Found " + str(count) + " messages.")

# --------------------------------------------------------------------------- #

    # Print initial screen
    ui.print_screen()

    # start input coroutine
    asyncio.get_event_loop().create_task(input_handler())

@asyncio.coroutine
def input_handler():
    yield from client.wait_until_ready()

    while True:
        with term.location(len(client.get_prompt()) + 7, term.height - 2):
            user_input = input().rstrip()

        # If input is blank, don't do anything
        if user_input == '': continue

        # Check if input is a command
        elif user_input[0] == prefix:
            # Strip the prefix
            user_input = user_input[1:]

            # Check if contains a space
            if ' ' in user_input:
                # Split into command and argument
                command,arg = user_input.split(" ", 1)
                if command == "server":
                    # TODO: check if arg is a valid server
                    client.set_current_server(arg)
                    client.set_current_channel(client.get_server(arg).default_channel)
                    ui.clear_screen()
                elif command == "channel" or command == 'c':
                    # TODO: check if arg is a valid channel
                    client.set_current_channel(arg)
                    client.set_prompt(arg)

            # Else we must have only a command, no argument
            else:
                command = user_input
                # if command == "help": print_help()
                if command == "clear": ui.clear_screen()
                if command == "quit": kill()
                if command == "exit": kill()
        
        # This must not be a command...
        else: 
            pass
            # If all options have been exhausted, it must be character
            yield from client.send_message(client.get_current_channel(), user_input)

        # Update the screen
        ui.print_screen()

        # while the screen is printing, sleep this thread
        yield from asyncio.sleep(0.1)

        

# called whenever the client receives a message (from anywhere)
@client.event
async def on_message(message):

    # find the server/channel it belongs to and add it
    for server_log in server_log_tree:
        if server_log.get_name == message.server.name:
            for channel_log in server_log.get_logs():
                if channel_log.get_name() == message.channel.name:
                    channel_log.append(message)

    # redraw the screen
    ui.print_screen()

# kills the program and all its elements gracefully
def kill():
    ui.clear_screen()
    quit()

client.run(sys.argv[1], bot=False)
