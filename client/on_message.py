import asyncio
from ui.ui_utils import calc_mutations
from utils.log import log
from utils.globals import gc

async def on_incoming_message(msg):

    # TODO: make sure it isn't a private message

    # find the server/channel it belongs to and add it
    doBreak = False
    for server_log in gc.server_log_tree:
        if server_log.get_server() == msg.server:
            for channel_log in server_log.get_logs():
                if channel_log.get_channel() == msg.channel:
                    channel_log.append(await calc_mutations(msg))
                    if channel_log.get_channel() is not gc.client.get_current_channel():
                        if msg.server.me.mention in msg.content:
                            channel_log.mentioned_in = True
                        else:
                            channel_log.unread = True
                    doBreak = True
                    break
        if doBreak:
            break

    # redraw the screen
    gc.ui.doUpdate = True
