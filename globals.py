from client import Client
from blessings import Terminal
from settings import *

client = Client(max_messages=MAX_MESSAGES)
term = Terminal()
server_log_tree = []
input_buffer = []
# kills the program and all its elements gracefully
def kill():
    import asyncio
    try: client.close()
    except: pass
    try: asyncio.get_event_loop().close()
    except: pass
    quit()


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
    # colors async defined wrong. We'll be nice and just return white.
    return term.white
