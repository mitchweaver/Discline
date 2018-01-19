import asyncio
from utils.settings import settings
from utils.globals import gc

async def is_typing_handler():
    # user specified setting in settings.py
    if not settings["send_is_typing"]: return
    
    is_typing = False
    while True:
        # if typing a message, display '... is typing'
        if not is_typing:
            if len(gc.input_buffer) > 0 and gc.input_buffer[0] is not settings["prefix"]:
                await gc.client.send_typing(gc.client.get_current_channel())
                is_typing = True
        elif len(gc.input_buffer) == 0 or gc.input_buffer[0] is settings["prefix"]:
            is_typing = False
        
        await asyncio.sleep(0.5)

