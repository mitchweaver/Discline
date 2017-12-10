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

# returns a "Channel" object from the given string
async def string2channel(channel):
    for srv in client.servers:
        if srv.name == channel.server.name:
            for chan in srv.channels:
                if chan.name == channel:
                    return chan

# returns a "Channellog" object from the given string
async def get_channel_log(channel):
    for srvlog in server_log_tree:
        if srvlog.get_name().lower() == channel.server.name.lower():
            for chanlog in srvlog.get_logs():
                if chanlog.get_name().lower() == channel.name.lower():
                    return chanlog

# returns a "Channellog" from a given "Channel"
async def chan2log(chan):
    for srvlog in server_log_tree:
        if srvlog.get_name().lower() == chan.server.name.lower():
            for clog in srvlog.get_logs():
                if clog.get_name().lower() == chan.name.lower():
                    return clog
 
# returns a "Serverlog" from a given "Server"
async def serv2log(serv):
    for srvlog in server_log_tree:
        if srvlog.get_name().lower() == serv.name.lower():
            return srvlog

# takes in a string, returns the appropriate term.color
async def get_color(string):
    arg = string.strip().lower()
    if arg == "white":   return term.white
    if arg == "black":   return term.black
    if arg == "red":     return term.red
    if arg == "blue":    return term.blue
    if arg == "yellow":  return term.yellow
    if arg == "cyan":    return term.cyan
    if arg == "magenta": return term.magenta
    if arg == "green":   return term.green

    if arg == "on_white":   return term.on_white
    if arg == "on_black":   return term.on_black
    if arg == "on_red":     return term.on_red
    if arg == "on_blue":    return term.on_blue
    if arg == "on_yellow":  return term.on_yellow
    if arg == "on_cyan":    return term.on_cyan
    if arg == "on_magenta": return term.on_magenta
    if arg == "on_green":   return term.on_green

    if arg == "blink_white":   return term.blink_white
    if arg == "blink_black":   return term.blink_black
    if arg == "blink_red":     return term.blink_red
    if arg == "blink_blue":    return term.blink_blue
    if arg == "blink_yellow":  return term.blink_yellow
    if arg == "blink_cyan":    return term.blink_cyan
    if arg == "blink_magenta": return term.blink_magenta
    if arg == "blink_green":   return term.blink_green


    # if we're here, someone has one of their settings.py
    # colors defined wrong. We'll be nice and just return white.
    return term.normal + term.white
