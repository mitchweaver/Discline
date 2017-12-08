import asyncio
from settings import SEND_IS_TYPING, PREFIX
from utils.globals import client, input_buffer

async def is_typing_handler():
    # user specified setting in settings.py
    if not SEND_IS_TYPING: return
    
    is_typing = False
    while True:
        # if typing a message, display '... is typing'
        if not is_typing:
            if len(input_buffer) > 0 and input_buffer[0] is not PREFIX:
                await client.send_typing(client.get_current_channel())
                is_typing = True
        elif len(input_buffer) == 0 or input_buffer[0] is PREFIX:
            is_typing = False
        
        await asyncio.sleep(0.5)

