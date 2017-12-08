from client.client import Client
from blessings import Terminal
from settings import *
from sys import exit

client = Client(max_messages=MAX_MESSAGES)
term = Terminal()
server_log_tree = []
input_buffer = []
user_input = ""

# kills the program and all its elements gracefully
def kill():
    # attempt to cleanly close our loops
    import asyncio
    try: client.close()
    except: pass
    try: asyncio.get_event_loop().close()
    except: pass
    try:# since we're exiting, we can be nice and try to clear the screen
        from os import system
        system("clear")
    except: pass
    exit()

# returns a "Channel" object from the given strings
async def get_channel(server, channel):
    for srv in client.servers:
        if srv.name == server.name:
            for chan in srv.channels:
                if chan.name == channel.name:
                    return chan

# returns a "Channellog" object from the given strings
async def get_channel_log(server, channel):
    for srvlog in server_log_tree:
        if srvlog.get_name() == server.name:
            for chanlog in srvlog.get_logs():
                if chanlog.get_name() == channel.name:
                    return chanlog

# takes in a string, returns the appropriate term.color
async def get_color(string):
    if string == "white":   return term.white
    if string == "black":   return term.black
    if string == "red":     return term.red
    if string == "blue":    return term.blue
    if string == "yellow":  return term.yellow
    if string == "cyan":    return term.cyan
    if string == "magenta": return term.magenta
    if string == "green":   return term.green

    if string == "on_white":   return term.on_white
    if string == "on_black":   return term.on_black
    if string == "on_red":     return term.on_red
    if string == "on_blue":    return term.on_blue
    if string == "on_yellow":  return term.on_yellow
    if string == "on_cyan":    return term.on_cyan
    if string == "on_magenta": return term.on_magenta
    if string == "on_green":   return term.on_green

    # if we're here, someone has one of their settings.py
    # colors defined wrong. We'll be nice and just return white.
    return term.normal + term.white
