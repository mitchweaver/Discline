from ui import print_screen
from globals import *
from settings import *


async def calc_mutations(msg):
    text = ""

    # if the message is a file, extract the discord url from it
    # if len(msg.attachments) > 0:
    #     url = msg.attachments[0]
      
    #     # if there is text with the attachment, add that too
    #     if len(msg.clean_content) > 1: # not sure what this char is, its not \n
    #         text = msg.clean_content + url
    #     else: text = url

    # # else it must just be a normal message
    # else: 
    # text = msg.clean_content
   
    msg.content = msg.clean_content + text

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
