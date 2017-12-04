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
