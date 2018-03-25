from sys import exit
from blessings import Terminal
from utils.settings import settings
import sys

NO_SETTINGS=False
try:
    if sys.argv[1] == "--store-token" or sys.argv[1] == "--token":
        NO_SETTINGS=True
except IndexError: 
    pass

class GlobalsContainer:
    def __init__(self):
        self.term = Terminal()
        self.client = None
        self.server_log_tree = []
        self.input_buffer = []
        self.user_input = ""
        self.channels_entered = []

    def initClient(self):
        from client.client import Client
        if NO_SETTINGS:
            messages=100
        else:
            messages=settings["max_messages"]
        self.client = Client(max_messages=messages)

gc = GlobalsContainer()

# kills the program and all its elements gracefully
def kill():
    # attempt to cleanly close our loops
    import asyncio
    try: gc.client.close()
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
    for srv in gc.client.servers:
        if srv.name == channel.server.name:
            for chan in srv.channels:
                if chan.name == channel:
                    return chan

# returns a "Channellog" object from the given string
async def get_channel_log(channel):
    for srvlog in gc.server_log_tree:
        if srvlog.get_name().lower() == channel.server.name.lower():
            for chanlog in srvlog.get_logs():
                if chanlog.get_name().lower() == channel.name.lower():
                    return chanlog

# returns a "Channellog" from a given "Channel"
async def chan2log(chan):
    for srvlog in gc.server_log_tree:
        if srvlog.get_name().lower() == chan.server.name.lower():
            for clog in srvlog.get_logs():
                if clog.get_name().lower() == chan.name.lower():
                    return clog
 
# returns a "Serverlog" from a given "Server"
async def serv2log(serv):
    for srvlog in gc.server_log_tree:
        if srvlog.get_name().lower() == serv.name.lower():
            return srvlog

# takes in a string, returns the appropriate term.color
async def get_color(string):
    arg = string.strip().lower()

    if arg == "white":   return gc.term.white
    if arg == "black":   return gc.term.black
    if arg == "red":     return gc.term.red
    if arg == "blue":    return gc.term.blue
    if arg == "yellow":  return gc.term.yellow
    if arg == "cyan":    return gc.term.cyan
    if arg == "magenta": return gc.term.magenta
    if arg == "green":   return gc.term.green

    if arg == "on_white":   return gc.term.on_white
    if arg == "on_black":   return gc.term.on_black
    if arg == "on_red":     return gc.term.on_red
    if arg == "on_blue":    return gc.term.on_blue
    if arg == "on_yellow":  return gc.term.on_yellow
    if arg == "on_cyan":    return gc.term.on_cyan
    if arg == "on_magenta": return gc.term.on_magenta
    if arg == "on_green":   return gc.term.on_green

    if arg == "blink_white":   return gc.term.blink_white
    if arg == "blink_black":   return gc.term.blink_black
    if arg == "blink_red":     return gc.term.blink_red
    if arg == "blink_blue":    return gc.term.blink_blue
    if arg == "blink_yellow":  return gc.term.blink_yellow
    if arg == "blink_cyan":    return gc.term.blink_cyan
    if arg == "blink_magenta": return gc.term.blink_magenta
    if arg == "blink_green":   return gc.term.blink_green


    # if we're here, someone has one of their settings.yaml
    # colors defined wrong. We'll be nice and just return white.
    return gc.term.normal + gc.term.white
