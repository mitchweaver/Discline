#!/usr/bin/python3.6
import sys
import asyncio
from os import system

import discord

from input.input_handler import input_handler, key_input
from input.typing_handler import is_typing_handler
from ui.ui import print_screen
from ui.text_manipulation import calc_mutations
from utils.print_utils.help import print_help
from utils.print_utils.print_utils import *
from utils.globals import *
from utils.updates import check_for_updates
from utils import hidecursor
from client.serverlog import ServerLog
from client.channellog import ChannelLog
from client.on_message import on_incoming_message
from client.client import Client
from settings import *

# check if using python 3.5+
# TODO: this still fails if they're using python2
if sys.version_info >= (3, 5): pass
else:
    print(term.red + "Sorry, but this requires python 3.5+")
    quit()

@client.event
async def on_ready():
    await client.wait_until_login()

    # clear screen while the client loads
    system("clear")

    # completely hide the system's cursor
    await hidecursor.hide_cursor()

    # these values are set in settings.py
    if DEFAULT_PROMPT is not None:
        client.set_prompt(DEFAULT_PROMPT.lower())
    else: client.set_prompt('~')

    if DEFAULT_SERVER is not None:
        client.set_current_server(DEFAULT_SERVER)
        if DEFAULT_CHANNEL is not None:
            client.set_current_channel(DEFAULT_CHANNEL.lower())
            client.set_prompt(DEFAULT_CHANNEL.lower())

    if DEFAULT_GAME is not None:
        await client.change_presence(game=discord.Game(name=DEFAULT_GAME), \
                                        status=None,afk=False)

    # --------------- INIT SERVERS ----------------------------------------- #
    print("Welcome to " + term.cyan + "Terminal Discord" + term.normal + "!")
    await print_line_break()
    await print_user()
    await print_line_break()
    print("Initializing... \n")
    try: sys.stdout.flush()
    except: pass

    # list to store our "ChannelLog" data type
    for server in client.servers:
        serv_logs = []
        count = 0
        print("loading " + term.magenta + server.name + term.normal + " ...")
        for channel in server.channels:
            if channel.type == discord.ChannelType.text:
                    if channel.permissions_for(server.me).read_messages:
                        try: # try/except in order to 'continue' out of multiple for loops
                            for serv_key in CHANNEL_IGNORE_LIST:
                                if serv_key.lower() == server.name.lower():
                                    for name in CHANNEL_IGNORE_LIST[serv_key]:
                                        if channel.name.lower() == name.lower():
                                            raise Found

                            print("    loading " + term.yellow + channel.name + term.normal)
                            channel_log = []
                            try:
                                async for msg in client.logs_from(channel, limit=MAX_LOG_ENTRIES):
                                    count+=1
                                    channel_log.insert(0, await calc_mutations(msg))
                                serv_logs.append(ChannelLog(channel, channel_log))
                            except:
                                print("Error loading logs from channel: " + \
                                    channel.name + " in server: " + server.name)
                                continue
                        except: continue

        print("\n - Channels loaded! Found " + str(count) + " messages. \n")

        # add the channellog to the tree
        server_log_tree.append(ServerLog(server, serv_logs)) 
            
        if DEBUG:
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



# called whenever the client receives a message (from anywhere)
@client.event
async def on_message(message):
    await on_incoming_message(message)

@client.event
async def on_message_edit(msg_old, msg_new):
    msg_new.content = msg_new.content + " *(edited)*"

    # redraw the screen
    await print_screen()

@client.event
async def on_message_delete(msg):
    # TODO: PM's have 'None' as a server -- fix this later
    if msg.server is None: return

    try:
        for serverlog in server_log_tree:
            if serverlog.get_server() == msg.server:
                for channellog in serverlog.get_logs():
                    if channellog.get_channel()== msg.channel:
                        channellog.get_logs().remove(msg)
                        await print_screen()
                        return
    except:
        # if the message cannot be found, an exception will be raised
        # this could be #1: if the message was already deleted,
        # (happens when multiple calls get excecuted within the same time)
        # or the user was banned, (in which case all their msgs disappear)
        pass


def main():
    check_for_updates()
   
    # start the client coroutine
    TOKEN=""
    try: TOKEN=sys.argv[1]
    except IndexError:
        print(term.red + "Error: You did not specify a token! Please see the README.md")
        quit()

    print("Starting...")

    # start the client
    try: client.run(TOKEN, bot=False)
    except SystemExit: pass
    except KeyboardInterrupt: pass

    # if we are here, the client's loop was cancelled or errored, or user exited
    try: kill()
    except: 
        # if our cleanly-exit kill function failed for whatever reason,
        # make sure we at least exit uncleanly
        quit()

if __name__ == "__main__": main()
