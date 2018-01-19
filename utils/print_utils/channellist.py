from os import system
from discord import ChannelType
from ui.ui import clear_screen, set_display
from utils.globals import gc

async def print_channellist():
    if len(gc.client.servers) == 0:
        set_display(gc.term.red + "Error: You are not in any servers.")
        return
    
    if len(gc.client.get_current_server().channels) == 0:
        set_display(gc.term.red + "Error: Does this server not have any channels?" + gc.term.normal)
        return

    buffer = []
    for channel in gc.client.get_current_server().channels:
        if channel.type == ChannelType.text:
            name = channel.name
            name = name.replace("'", "")
            name = name.replace('"', "")
            name = name.replace("`", "")
            buffer.append(name + "\n")

    await clear_screen()
    system("echo '" + gc.term.cyan + "Available Channels in " \
           + gc.term.magenta + gc.client.get_current_server_name() + ": \n" \
           + "---------------------------- \n \n" \
           + gc.term.yellow + "".join(buffer) \
           + gc.term.green + "~ \n" \
           + gc.term.green + "~ \n" \
           + gc.term.green + "(press \'q\' to quit this dialog) \n" \
           + "' | less -R")

