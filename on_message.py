from ui import print_screen
from globals import *
from settings import *

async def calc_mutations(msg):
    text = ""

    # if the message is a file, extract the discord url from it
    try:
        json = str(msg.attachments[0]).split("'")
        text = json[5]
        msg.content = text
        return msg
    except:
        return msg





async def on_incoming_message(msg):

    # TODO: make sure it isn't a private message

    # find the server/channel it belongs to and add it
    for server_log in server_log_tree:
        if server_log.get_server() == msg.server:
            for channel_log in server_log.get_logs():
                if channel_log.get_channel() == msg.channel:
                    channel_log.append(await calc_mutations(msg))
                    break

    # redraw the screen
    await print_screen()
