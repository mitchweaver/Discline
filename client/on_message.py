from ui.ui import print_screen
from utils.globals import *
from settings import *
from ui.text_manipulation import calc_mutations

async def on_incoming_message(msg):

    # TODO: make sure it isn't a private message
    
    # find the server/channel it belongs to and add it
    try: # (note: the try/except here is to be able to break out of the double for loop)
        for server_log in server_log_tree:
            if server_log.get_server() == msg.server:
                for channel_log in server_log.get_logs():
                    if channel_log.get_channel() == msg.channel:
                        
                        # check if the message is a "user has pinned..." message
                        if msg.type == MessageType.pins_add:
                            name = ""
                            if msg.author.nick is not None and \
                               msg.author.nick != "":
                                name = msg.author.nick
                            else: name = msg.author.name
                            msg.content = "📌 " + name + " has pinned a message to this channel."
                            channel_log.append(msg)
                        else:
                            channel_log.append(await calc_mutations(msg))
                        
                        if channel_log.get_channel() is not client.get_current_channel():
                            channel_log.unread = True
                        raise Found
    except:
        # redraw the screen
        await print_screen()
