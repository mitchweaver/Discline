import asyncio
from settings import *
from utils.globals import client, input_buffer

async def is_typing_handler():
    # user specified setting in settings.py
    if not settings["send_is_typing"]: return
    
    is_typing = False
    while True:
        # if typing a message, display '... is typing'
        if not is_typing:
            if len(input_buffer) > 0 and input_buffer[0] is not settings["prefix"]:
                await client.send_typing(client.get_current_channel())
                is_typing = True
        elif len(input_buffer) == 0 or input_buffer[0] is settings["prefix"]:
            is_typing = False
        
        await asyncio.sleep(0.5)

