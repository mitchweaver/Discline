#!/usr/bin/python3
############################################
#                                          #
# Discline                                 #
#                                          #
# http://github.com/MitchWeaver/Discline   #
#                                          #
# Licensed under GNU GPLv3                 #
#                                          #
############################################ 

import sys
import asyncio
from os import system
import discord
from input.input_handler import input_handler, key_input, init_input
from input.typing_handler import is_typing_handler
from ui.ui import print_screen
from ui.text_manipulation import calc_mutations
from utils.print_utils.help import print_help
from utils.print_utils.print_utils import *
from utils.globals import *
from utils.settings import settings
from utils.updates import check_for_updates
from utils.token_utils import get_token
from utils import hidecursor
from client.serverlog import ServerLog
from client.channellog import ChannelLog
from client.on_message import on_incoming_message
from client.client import Client

# check if using python 3.5+
# TODO: this still fails if they're using python2
if sys.version_info >= (3, 5): pass
else:
    print(term.red + "Sorry, but this requires python 3.5+" + term.normal)
    quit()

init_complete = False

@client.event
async def on_ready():
    await client.wait_until_login()
    
    # completely hide the system's cursor
    await hidecursor.hide_cursor()

    # these values are set in settings.yaml
    if settings["default_prompt"] is not None:
        client.set_prompt(settings["default_prompt"].lower())
    else: client.set_prompt('~')

    if settings["default_server"] is not None:
        client.set_current_server(settings["default_server"])
        if settings["default_channel"] is not None:
            client.set_current_channel(settings["default_channel"].lower())
            client.set_prompt(settings["default_channel"].lower())

    if settings["default_game"] is not None:
        await client.change_presence(game=discord.Game(name=settings["default_game"]), \
                                        status=None,afk=False)

    # --------------- INIT SERVERS ----------------------------------------- #
    print("Welcome to " + term.cyan + "Terminal Discord" + term.normal + "!")
    await print_line_break()
    await print_user()
    await print_line_break()
    print("Initializing... \n")
    try: sys.stdout.flush()
    except: pass

    for server in client.servers:
        serv_logs = []
        count = 0
        print("loading " + term.magenta + server.name + term.normal + " ...")
        for channel in server.channels:
            if channel.type == discord.ChannelType.text:
                    if channel.permissions_for(server.me).read_messages:
                        try: # try/except in order to 'continue' out of multiple for loops
                            for serv_key in settings["channel_ignore_list"]:
                                if serv_key["server_name"].lower() == server.name.lower():
                                    for name in serv_key["ignores"]:
                                        if channel.name.lower() == name.lower():
                                            raise Found

                            print("    loading " + term.yellow + channel.name + term.normal)
                            channel_log = []
                            try:
                                async for msg in client.logs_from(channel, limit=settings["max_log_entries"]):
                                    count+=1
                                    channel_log.insert(0, await calc_mutations(msg))
                                serv_logs.append(ChannelLog(channel, channel_log))
                            except:
                                print(term.red + "Error loading logs from channel: " + \
                                    channel.name + " in server: " + server.name + term.normal)
                                continue
                        except: continue

        print("\n - Channels loaded! Found " + str(count) + " messages. \n")

        # add the channellog to the tree
        server_log_tree.append(ServerLog(server, serv_logs)) 
            
        if settings["debug"]:
            for slog in server_log_tree:
                for clog in slog.get_logs():
                    print(slog.get_name() + " ---- " + clog.get_name())

    # start our own coroutines
    try: asyncio.get_event_loop().create_task(key_input())
    except SystemExit: pass
    except KeyboardInterrupt: pass
    try: asyncio.get_event_loop().create_task(input_handler())
    except SystemExit: pass
    except KeyboardInterrupt: pass
    try: asyncio.get_event_loop().create_task(is_typing_handler())
    except SystemExit: pass
    except KeyboardInterrupt: pass

    # Print initial screen
    await print_screen()

    global init_complete
    init_complete = True

# called whenever the client receives a message (from anywhere)
@client.event
async def on_message(message):
    await client.wait_until_ready()
    if init_complete:
        await on_incoming_message(message)

@client.event
async def on_message_edit(msg_old, msg_new):
    await client.wait_until_ready()
    msg_new.content = msg_new.content + " *(edited)*"

    if init_complete:
        await print_screen()

@client.event
async def on_message_delete(msg):
    await client.wait_until_ready()
    # TODO: PM's have 'None' as a server -- fix this later
    if msg.server is None: return

    try:
        for serverlog in server_log_tree:
            if serverlog.get_server() == msg.server:
                for channellog in serverlog.get_logs():
                    if channellog.get_channel()== msg.channel:
                        channellog.get_logs().remove(msg)
                        if init_complete:
                            await print_screen()
                        return
    except:
        # if the message cannot be found, an exception will be raised
        # this could be #1: if the message was already deleted,
        # (happens when multiple calls get excecuted within the same time)
        # or the user was banned, (in which case all their msgs disappear)
        pass


def main():
    # start the client coroutine
    TOKEN=""
    try: 
        if sys.argv[1] == "--help" or sys.argv[1] == "-help":
            from utils.print_utils.help import print_help
            print_help()
            quit()

        if sys.argv[1] == "--skeleton" or sys.argv[1] == "--copy-skeleton":
           from settings import copy_skeleton
           copy_skeleton()
           quit()

        if sys.argv[1] == "--token" or sys.argv[1] == "--store-token":
            from utils.token_utils import  store_token
            store_token()
            quit()

    except IndexError:
        quit()

    check_for_updates()
    token = get_token()
    init_input()
    
    print(term.yellow("Starting..."))

    # start the client
    try: client.run(token, bot=False)
    except SystemExit: pass
    except KeyboardInterrupt: pass

    # if we are here, the client's loop was cancelled or errored, or user exited
    try: kill()
    except: 
        # if our cleanly-exit kill function failed for whatever reason,
        # make sure we at least exit uncleanly
        quit()

if __name__ == "__main__": main()
